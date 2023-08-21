from django.urls import path,include
from .views import LoginView,RegisterView,AccountView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
urlpatterns = [ 
  path("user", AccountView.as_view(), name="accounts"),
  path("login/", LoginView.as_view(), name="login"),
  path('logout/', LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
  path("register/", RegisterView.as_view(), name="register")
]

