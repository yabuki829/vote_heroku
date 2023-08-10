# 投票するためのform.pyです


from django import forms
from ..models import Vote

# 投票するのに必要なひつような情報は

# userid 
# vote_id
# choice_id 選択肢のid の三つがあればok

