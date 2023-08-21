from django.shortcuts import render
from ..models import Vote,Choice,User,VoteComment
from django.views.generic import View
from django.shortcuts import redirect
from django.core.paginator import Paginator
from ..methods import random
class VoteListView(View):

  def get(self,request):
    page = request.GET.get('page') # 表示したいページ
    if page == None :
      page = 1
    page_cnt = 10 #一画面あたり10コ表示する
    onEachSide = 3 #選択ページの両側には3コ表示する
    onEnds = 2 #左右両端には2コ表示する

    data = Vote.objects.filter(isLimitedRelease=False).prefetch_related('choices').order_by('-createdAt')
    data_page = Paginator(data,page_cnt)
    data_p = data_page.get_page(page)

    data_p = data_page.get_page(page)
    data_list = list(data_p.paginator.get_elided_page_range(page, on_each_side=onEachSide, on_ends=onEnds)) 
    data = {'data_p':data_p,'data_list':data_list}
    return render(request,"voteList.html",data)


class VoteDetailsView(View):
  def get(self,request,pk):
    vote = Vote.objects.prefetch_related('choices').get(id=pk)
    user = self.request.user
    count = len(vote.numberOfVotes.all())
   
    # コメントを取得する
    comments = VoteComment.objects.filter(vote=vote.id).order_by('-createdAt')

    print("コメント取得できていますか？")
    
    print(comments) 
    context = {
      'vote': vote,
      "request": request,
      "count":count,
      "user":user,
      "comments":comments
    } 
    print(user,"user")
    
    if self.request.user.is_anonymous:
      user_id = request.COOKIES.get("id")
      if user_id != None:
        print("ログインしてないが、user_idがあるuserです")
        user = User.objects.get(id=user_id)
      else:
        print("ログインしてないかつ、user_idがないuserです")
        return render(request,"voteDetails.html",context)
    # userが投票しているかを確認する

    print("AAAAAAAAAAAAAAAAAAAA")
    
    # 投票していれば、
    # isVote  = true
    context = {
      'vote': vote,
      "request": request,
      "count":count,
      "user":user,
      "comments":comments
    } 
    # 投票の%をデータとして持っておく   
    if user in vote.numberOfVotes.all():
      sum = len(vote.numberOfVotes.all())
      choice_percent = []
      print( vote.choices.all())  
      for choice in vote.choices.all():
        choice_user_count = len(choice.votedUserCount.all())
        
        if  len(choice.votedUserCount.all()) != 0:
          choice_percent.append( round((choice_user_count  / sum)  * 100 , 1))
        else: 
          choice_percent.append( 0)
    
      print(choice_percent,"%です")
      context["choices_percent_list"] = choice_percent

    return render(request,"voteDetails.html",context)

  def post(self,request,pk):
    print(pk,"投稿に投票します")


    choice_id = request.POST.get('choice-id')
    # ログインしていない場合
    if self.request.user.is_anonymous:
      ip = self.get_client_ip(request)
      
      # cookieにuser_idがあればそのidのuserを取得する

      user_id = request.COOKIES.get("id")
      if user_id == None:
      # 仮のアカウントを作成する
        print("ログインしてないかつ、user_idがないuserです")
      
        # userを作成する
        # 作成していないuser_idを探す
      
        user = User.objects.create(active=False)
        # ここでuser_idをCookieに保存しておく
        print(user,"userを作成しました")
        vote = Vote.objects.get(id=pk)
        response = redirect( "details",vote.id )
        response.set_cookie(
            "id",
            user.id,
            httponly=True,
            secure=True,
            path='/',
            samesite="None"
          )
        print("C")
        # 投票する
        print("ユーザー",user)
        
        print("D")
        choice = Choice.objects.get(id=choice_id)
        choice.votedUserCount.add(user)
        vote.numberOfVotes.add(user)
        print("投票しました")

        return response
      else:
        print("ログインしてないが、user_idがあるuserです")
        user = User.objects.get(id=user_id)
        vote = Vote.objects.get(id=pk)
        choice = Choice.objects.get(id=choice_id)
        choice.votedUserCount.add(user)
        vote.numberOfVotes.add(user)
        print(choice)
        return redirect( "details",vote.id )

        # 'user_id'という名前のCookieにユーザーIDを設定
       
    else:
       # ログインしている場合
      print("ログインしているuserです")
      vote = Vote.objects.get(id=pk)
      choice = Choice.objects.get(id=choice_id)
      choice.votedUserCount.add(self.request.user)
      vote.numberOfVotes.add(self.request.user)
      print(choice)
    return redirect( "details",vote.id )

  def get_client_ip(cls, request):
    if not request or not request.META:
        # METAが含まれていない場合は取得できない
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    ip = None
    if xff:
        # 転送要素がある場合は転送経路の先頭を設定
        ip = xff.split(",")[0]
    else:
        # 通常のIPアドレス
        ip = request.META.get("REMOTE_ADDR")
    return ip

class PostView(View):
  def get(self,request):
    print("投稿画面")
    return render(request,"post.html")

  def post(self,request):
    print("投稿します")
    print(request.POST)
    post_type = request.POST["post_type"]

    # 限定公開
    if self.request.user.is_anonymous:
      user_id = request.COOKIES.get("id")
      if user_id != None:
        print("ログインしていないがuseridのあるユーザーです")
        user = User.objects.get(id=user_id)
      else:
        print("ログインしていないかつ、useridのないユーザーです")
        user_id = random.create_string(10)
        user = User.objects.create(user_id=user_id ,active=False)
    else:
      print("ログインしているユーザーです")
      user = self.request.user
    print("ユーザー",user)
    if post_type == "limited":
      vote = Vote.objects.create(user=user,questionText=request.POST["questionText"],isLimitedRelease=True)

    # 全体公開
    if post_type == "public":
      vote = Vote.objects.create(user=user,questionText=request.POST["questionText"],isLimitedRelease=False)
    # 選択を作成する

    choices = []
    for choice in request.POST.getlist('choice'):
      choice_obj = Choice.objects.create(vote=vote,text=choice)

    if self.request.user.is_anonymous:
        response = redirect( "details",vote.id )
        response.set_cookie(
            "id",
            user.id,
            httponly=True,
            secure=True,
            path='/',
            samesite="None"
          )
        return response
    
    return redirect( "details",vote.id )


# VoteのコメントのView
class VoteCommentView(View):

  def post(self,request,pk):
    vote = Vote.objects.get(pk=pk)
    VoteComment.objects.create(title=self.request.POST["comment"],user=self.request.user,vote=vote)

    return redirect( "details",vote.id )





class DeleteVoteView(View):
  def get(self,request,pk):
    # userがログインしていなければ元のページに戻す
    # vote.userとself.request.userが一致すれば表示する
    if self.request.user.is_anonymous :
      return redirect( "home" )

    vote = Vote.objects.get(pk=pk)

    if vote.user != self.request.user:
      return redirect( "home" )

    context = {
      "vote":vote
    }
    return render(request,"delete.html",context)

  def post(self,request,pk):
    print("削除します")
    if self.request.user.is_anonymous :
      return redirect( "home" )
    vote = Vote.objects.get(pk=pk)

    if vote.user != self.request.user:
      return redirect( "home" )

    vote.delete()

    return redirect("accounts")
