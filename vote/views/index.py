from django.shortcuts import render
from ..models import User
from django.views.generic import View
# Create your views here.
from django.contrib.auth.hashers import make_password
def index(request):
  users = User.objects.all()
  
  return render(request, 'index.html')

