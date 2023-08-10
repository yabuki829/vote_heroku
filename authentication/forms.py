from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from vote.models import User



class UserCreateForm(UserCreationForm):
    class Meta:
       model = User
       fields = ("username", "user_id")

class LoginForm(AuthenticationForm):
     class Meta:
       model = User
       fields = ("user_id","password")