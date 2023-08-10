from django.urls import path,include
from .views import ThreadView
urlpatterns = [ 
  path("",ThreadView.as_view(),name="thread"),

]
