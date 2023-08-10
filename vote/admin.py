from django.contrib import admin

# Register your models here.
from .models import Vote,Blog,Choice,User,VoteComment

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 0
 
class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    list_display = ('questionText', 'createdAt')

admin.site.register(Vote,QuestionAdmin)

admin.site.register(Blog)
admin.site.register(User)

admin.site.register(VoteComment)