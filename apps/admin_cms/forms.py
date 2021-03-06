from django import forms
from apps.forms import FormMinin

# 新闻内容验证
class NewsPubForm(forms.Form,FormMinin):
    title = forms.CharField(max_length=100, min_length=2, error_messages={"required": "新闻标签不能为空", "max_length" :"新闻标题超出最大长度100", "min_length": "标题最小长度为1个字符"})

    desc = forms.CharField(max_length=200, min_length=5, error_messages={"required": "新闻描术不能为空", "min_length": "新闻描术必须大于5个字符" ,"max_length": "新闻描述超出最大长度200"})

    tag_id = forms.IntegerField(error_messages={"required": "新闻标签不能为空"})

    thumbnail_url = forms.URLField(error_messages={"required": "缩略图不能为空"})

    content = forms.CharField(max_length=100000)
