from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from utils import json_status
from apps.news.models import NewTag, News
from django.http import QueryDict, JsonResponse
import os
from django.conf import settings
from qiniu import Auth
from .forms import NewsPubForm


# Create your views here.

@staff_member_required(login_url='/account/login')
def admin(request):

    return render(request,'admin/index.html')


@method_decorator([csrf_exempt,staff_member_required(login_url='/account/login')
],name="dispatch")
class NewTagView(View):

    def get(self,request):
        new_tags = NewTag.objects.filter(is_delete=True).all()

        return render(request,'admin/news/news_tag_manage.html',context={"new_tags":new_tags})


    def post(self, request):
        name = request.POST.get("name")
        if name and bool(name.strip()):
            # 判断是否存在
            new_tag_exists = NewTag.objects.filter(name=name).exists()
            if new_tag_exists:
                return json_status.params_error(message="添加的标签已经存在，请重新输入")
            # 添加数据
            res = NewTag.objects.create(name=name)
            return json_status.result(message="添加成功")
        return json_status.params_error(message="请输入正确的值")


    def put(self,request):
        print(request.body)         #b'tag_id=1&tag_name=%E6%8A%80'

        res = QueryDict(request.body)   #<QueryDict: {'tag_name': ['技'], 'tag_id': ['1']}>

        print(res)      #技
        tag_name = res.get("tag_name")
        tag_id = res.get("tag_id")
        if tag_id and tag_name:
            tag = NewTag.objects.filter(id=tag_id)

            if tag:
                new_tag_exists = NewTag.objects.filter(name=tag_name).exists()
                if new_tag_exists:
                    return json_status.params_error(message="添加的标签已经存在，请重新输入")
                tag.update(name=tag_name)

                return json_status.result(message="修改成功")

            return json_status.params_error(message="id或标签信息错误")

        return json_status.result(message="id或标签错误")

    def delete(self,request):

        res = QueryDict(request.body)

        tag_id = res.get("tag_id")
        if tag_id:
            tag = NewTag.objects.filter(id=tag_id)
            if tag:
                tag.update(is_delete=False)
                return json_status.result(message="删除成功")
            return json_status.params_error(message="id错误")
        return json_status.params_error(message="id错误")



@method_decorator([csrf_exempt,staff_member_required(login_url='/account/login')
],name="dispatch")
class NewsPubView(View):
    def get(self,request):
        news_tags = NewTag.objects.all()

        return render(request,'admin/news/news_pub.html',context={"news_tags":news_tags})

    def post(self,request):
        form = NewsPubForm(request.POST)                    #传入form验证
        if form.is_valid():                                 #通过form验证的
            title = form.cleaned_data.get("title")          #从form里拿到的
            desc = form.cleaned_data.get("desc")
            tag_id = form.cleaned_data.get("tag_id")
            thumbnail_url = form.cleaned_data.get("thumbnail_url")
            content = form.cleaned_data.get("content")
            print(title,desc,tag_id,thumbnail_url,content)
            tag = NewTag.objects.filter(id=tag_id).first()
            title_repete = News.objects.filter(title=title).exists() #查标题是否存在
            if tag and not title_repete:
                News.objects.create(title=title,desc=desc,tag=tag,content=content,thumbnail_url=thumbnail_url,author=request.user)
                return json_status.result(message="新闻添加成功")

            return json_status.params_error(message="新闻标题已经存在，请重新输入")

        return json_status.params_error(message=form.get_error())


# 安装pip install qiniu
def up_token(request):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = settings.ACCESS_KEY
    secret_key = settings.SECRET_KEY
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = settings.BUCKET_NAME
    # 上传到七牛后保存的文件名

    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name)
    print(token)
    return JsonResponse({"uptoken": token})


def upload_file(request):
    file = request.FILES.get("upload_file")
    print(file)                 #文件对象
    print(type(file))           #对象<class 'django.core.files.uploadedfile.InMemoryUploadedFile'>
                                # 小于2.5m方内存 ，大于2.5放磁盘
    print(file.name)            #文件名
    print(type(file.name))      #字符串
    file_name = file.name
    file_path = os.path.join(settings.MEDIA_ROOT,file_name)

    with open(file_path,'wb') as f:
        for chunk in file.chunks():
            f.write(chunk)
        # f.close()
        print(request.build_absolute_uri())
        # 返回当前视图http://192.168.160.130:8001/admin_cms/upload_file/

        file_url = request.build_absolute_uri(settings.MEDIA_URL+file_name)
        #返回http://192.168.160.130:8001 + /media/+file_name
        print(file_url)
    return json_status.result(data = {"file_url":file_url})
