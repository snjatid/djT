from django.shortcuts import render
from django.views import View
from .models import NewTag,News,NewsComment
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from apps.news.forms import NewsCommentForm
from utils import json_status
from apps.news.serializers import NewsCommentSerializers
from django.contrib.auth.decorators import login_required
from utils.decorators import ajax_login_required

def index(request):
    news_tags = NewTag.objects.filter(is_delete=True).all()
    # defer不查新闻内容字段,  select_related预先查询，会先执行
    newses = News.objects.defer("content").select_related("tag","author").filter(is_delete=True).all()
    content = {"news_tags":news_tags,"newses":newses}

    from datetime import datetime
    from django.utils.timezone import now
    print(datetime.now())       #2018-10-22 10:18:38.778725 系统当前时间
    print(now())                #2018-10-22 02:18:38.779494+00:00  会跟据settings里的时区默认减 8

    return render(request,'news/index.html',context=content)


def news_detail(request,news_id):
    try:
        print(news_id)
        # news = News.objects.filter(id=news_id, is_delete=True).first()#空值返回None
        news = News.objects.get(id=news_id)
        return render(request,"news/news_detail.html", context={"news":news})
    except News.DoesNotExist:
        # django对于找不到的url都会跳到这个页面，必须是settings.DEBUG = False
        raise Http404



@method_decorator([csrf_exempt, ajax_login_required], name='dispatch')
class AddNewsCommentView(View):
    def post(self,request):
        form = NewsCommentForm(request.POST)
        if form.is_valid():
            news_id = form.cleaned_data.get("news_id")
            content = form.cleaned_data.get("content")
            print(news_id,content)
            news = News.objects.filter(id = news_id).first()
            if news:
                res = NewsComment.objects.create(content=content,author=request.user,news=news)
                print("res:",res)
                serializer = NewsCommentSerializers(res)
                print("serializer",serializer.data)
                return json_status.result(message="添加成功",data=serializer.data)
            return json_status.params_error(message="新闻不存在")
        return json_status.params_error(message=form.get_error())

# 后端拿到新闻id 返回json 前 端遍历 restfull
def comment_list_with_news(request):
    news_id = request.GET.get("news_id")
    print(news_id)
    # 根据新闻的new_id晒对应的评论
    news = News.objects.filter(id=news_id).first()
    if news:
        # 获取当前新闻下所有的评论
        news_comments = news.comments.all()
        # print(news_comments)    #<QuerySet [<NewsComment: NewsComment object (1)>]>
        #values()将Queryset转为json
        # print(news_comments.values()) #<QuerySet [{'create_time': datetime.datetime(2018, 10, 23, 2, 22, 26, 674233, tzinfo=<UTC>), 'news_id': 1, 'author_id': 1, 'content': '这是新闻id为1的第一条评 论', 'id': 1}]>
        # news_comments = list(news_comments.values())
        # for news_comment in news_comments:
            # 每天条评论的json,反回的并没有做者，只有作者的id
            #{'content': '这是新闻id为1的第一条评 论', 'create_time': datetime.datetime(2018, 10, 23, 2, 22, 26, 674233, tzinfo= < UTC >),
            # print(news_comment)
        serializers = NewsCommentSerializers(news_comments,many=True)
        print(serializers)
        print("_____________________________")
        print(serializers.data)
        return json_status.result(message="OK",data=serializers.data)
    return json_status.params_error(message="新闻id找不到")




def search(request):
    return render(request,'news/search.html')


