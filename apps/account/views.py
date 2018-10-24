from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,reverse,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from .forms import LoginForm,RegisterForm,VerifyForm
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.utils.decorators import method_decorator
from utils.captcha.captcha import Captcha
from io import BytesIO
from utils import mccache
from utils.alisms import sms_send
from .models import User
from utils import json_status

# Create your views here.

#csrf_exempt  不验证csrf
#csrf_protect  验证csrf  类视图加装必须用@method_decorator
@method_decorator([csrf_exempt, ] , name="dispatch")
class LoginView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'account/login.html')

    def post(self,request):
        form = LoginForm(request.POST)
        # 登陆验证
        if form.is_valid():
            print(form.is_valid())
            telephone = form.cleaned_data.get("telephone",None)
            password = form.cleaned_data.get("password",None)
            remember = form.cleaned_data.get("remember",None)
            print(telephone,password,remember)

            #去数据库查是否正确
            user = authenticate(username = telephone,password=password)

            if user:
                #只有form登陆的时候才有用
                next_url = request.GET.get("next")
                if next_url:
                    return redirect(next_url)

                login(request,user)
                #session的默认有效期是浏览器关闭时失效

                if remember:
                    # None表示默认值 两周 0表示关闭浏览器失效
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)

                #return JsonResponse({"code": 200, "msg":"登陆成功"})
                return json_status.result(message = "登陆成功")

            #return JsonResponse({"code":1,"msg":"用户名或密码错误"})
            return json_status.params_error(message="用户名或密码错误")
        #return JsonResponse({"code":1,"msg" : form.get_error()})
        return json_status.params_error(message = form.get_error())


def logoutView(request):
    logout(request)

    return redirect(reverse("account:login"))



class RegisterView(View):
    def get(self,request,*args,**kwargs):
        return render(request,'account/register.html')

    def post(self,request):
        form = RegisterForm(request.POST)
        if form.is_valid() and form.check_data():
            telephone = form.cleaned_data.get("telephone")
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print("-----",telephone,username,password)
            # 写入数据库存
            user = User.objects.create_user(telephone = telephone,username=username,password=password)
            print("user",user)
            login(request,user)

            #return JsonResponse({"Code":200,"msg":"注册成功view"})
            return json_status.result(message="注册成功view")

        #return JsonResponse({"Code":1,"msg":form.get_error()})
        return json_status.params_error(message=form.get_error())


class ResetPasswordView(View):
    def get(self,request):
        return render(request,'account/resetpassword.html')

    def post(self,request):
        form = VerifyForm(request.POST)
        if form.is_valid() and form.verify():
            telephone = request.POST.get("telephone")
            sms_captcha = request.POST.get("sms_captcha")
            user = User.objects.filter(telephone=telephone)
            if user:
                return json_status.result(message="OK")

        return json_status.params_error(message=form.get_error())









def graph_captcha(request):
    # 获取验证码
    text,img = Captcha.gene_code()
    print(text)
    print(img)
    # 二进制字结流
    out = BytesIO()
    # 保存文件，保存完成后seek位置在后面
    img.save(out,'png')
    # 移动光标开始位置
    out.seek(0)

    resp =  HttpResponse(content_type="image/png")

    resp.write(out.read())

    mccache.set_key("graph_captcha",text)
    return resp

def sms_captcha(request):
#     1 获取手机号
    telephone= request.GET.get('telephone')
#     2 生成验证码
    captcha = Captcha.gene_text()
#     3 发送短信
#     ret = str(sms_send.send_sms(telephone, captcha), encoding='utf-8')
#     print(ret)

    # 4 加验证码到缓存,转换成小写存进去
    mccache.set_key(captcha.lower(),captcha.lower())
    print("手机号:{}验证码:{}".format(telephone,captcha))
    return JsonResponse({"Code":200})
    #JsonResponse() 返回标准的json，safe = False
    # return JsonResponse(ret,safe=False)

#