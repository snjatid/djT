from django import forms
from apps.forms import FormMinin

# 新闻评论验证

class NewsCommentForm(forms.Form,FormMinin):
    # 传入的新闻id
    news_id = forms.IntegerField(error_messages={"required": "新闻id不能为空"})
    # 传入的新闻的评论
    content = forms.CharField(error_messages= {"required": "新闻评论内容不能为空"})