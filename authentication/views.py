from django.shortcuts import render
from django.views.generic import View
# Create your views here.
from django.contrib.auth import login, authenticate
from .forms import LoginForm,UserCreateForm
from vote.models import User,Vote
from django.shortcuts import render, redirect

class LoginView(View):
  def get(self,request):
    form = LoginForm()
    params = {
      "form":form
    }
    return render(request,"login.html",params)

  def post(self,request):
    print("ログインします")
    form = LoginForm(request, data=request.POST)
    user_id = self.request.POST.get('user_id')
    password = self.request.POST.get('password')
    print(user_id,password)

    if form.is_valid():
        user = form.get_user()
        if user:
          
          login(request, user)
          print("ログインできました。")
          return redirect("/vote")
    else:
      print("バリデーションに失敗しました")
      form = LoginForm()
    params = {
      "form":form
    }
    return render(request,"login.html",params)


class RegisterView(View):
    def get(self,request):
      form = UserCreateForm()
      params = {
        "form":form
      }
      return render(request,"register.html",params)

   

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            form.save()
            #フォームから'username'を読み取る
            username = form.cleaned_data.get('user_id')
            #フォームから'password1'を読み取る
            password = form.cleaned_data.get('password1')
            print(username,password)
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('/')
        else: 
          print("バリデーションに失敗しました。")
        return render(request, 'register.html', {'form': form,})


# profileを表示する

class AccountView(View):
  def get(self,request):
    # もしログインしていなければlogin画面に飛ばす
    if self.request.user.is_anonymous:
      form = LoginForm()
      params = {
        "form":form
      }
      return redirect("/accounts/login")

    # self.requset.user が投稿したvoteを取得する
    vote = Vote.objects.filter(user=self.request.user)
    context = {
      "votes":vote
    }
    print(vote)
    return render(request,"account.html",context)
  def post(self,request):
    pass