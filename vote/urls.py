from django.urls import path,include
from .views import index,main
urlpatterns = [ 
  path("",index.index),
  path("vote/", main.VoteListView.as_view(), name="home"),
  path("vote/post/", main.PostView.as_view(), name="post"),
  path("vote/<str:pk>/", main.VoteDetailsView.as_view(), name="details"),
  path("vote/comment/<str:pk>/", main.VoteCommentView.as_view(), name="comment"),

]
