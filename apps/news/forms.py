from django import forms
from apps.forms import FormMinin

class NewsCommentForm(forms.Form,FormMinin):
    news_id = forms.IntegerField(error_messages={"required":"新闻id不能为空"})
    content = forms.CharField(error_messages={"required":"新闻内容不能为空"})