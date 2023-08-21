from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
from .methods import random
import uuid


def upload_profile_image_path(instance, filename):
    #jpg png などの拡張子の部分を取得する
    ext = filename.split('.')[-1]
    return '/'.join(['images/profiles',str(uuid.uuid4())+str(".")+str(ext)])

def upload_post_path(instance, filename):
    ext = filename.split('.')[-1]
    return '/'.join(['images/posts', str(uuid.uuid4())+str(".")+str(ext)])


class UserManager(BaseUserManager):
    def create_user(self, user_id, password=None):
        if not user_id:
            raise ValueError('Users must have an email address')

        user = self.model(
            user_id=user_id
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_id, password):
        user = self.create_user(
            user_id,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_id, password):
        user = self.create_user(
            user_id,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    ip = models.GenericIPAddressField(null=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 
    user_id = models.CharField(default=random.create_string(10), unique=True,max_length=20)
    username = models.CharField(max_length=30, default="No name")
    
    USERNAME_FIELD = 'user_id'
    objects = UserManager()


    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_label):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active




class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True) 

    def __str__(self) -> str:
       return self.title
    
class Vote(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    questionText = models.CharField(max_length=200)
    createdAt = models.DateTimeField(auto_now_add=True) 
    image = models.ImageField(blank=True, null=True, upload_to=upload_profile_image_path)
    #urlを知っている人のみ投票ができる
    isLimitedRelease = models.BooleanField(default=False)
    numberOfVotes = models.ManyToManyField(User, blank=True,related_name="numberOfVotes")
    pv = models.IntegerField(default=0)
    
    def __str__(self) -> str:
       return self.questionText

class VoteComment(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True) 
    vote = models.ForeignKey(Vote,  on_delete=models.CASCADE,related_name="comment")
    def __str__(self) -> str:
       return self.vote.questionText+"：　"+ self.title

class Choice(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4, editable=False)
    text = models.CharField(max_length=200)
    #誰がこの選択肢に投票したのか
    votedUserCount = models.ManyToManyField(User, blank=True)
    vote = models.ForeignKey(Vote,  on_delete=models.CASCADE,related_name="choices")

    def __str__(self) -> str:
       return self.text
