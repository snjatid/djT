from django import forms
from apps.forms import FormMinin
from utils import mccache

# 登陆验证
class LoginForm(forms.Form , FormMinin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={"max_length": "手机号太长","min_length":"手机号有点短","required":'手机号不能为空'})
    password = forms.CharField(max_length=20, min_length=6, error_messages={"max_length" : "密码长度有误","min_length":"密码长度太短","required":"密码不能为空"})

    remember = forms.BooleanField(required=False)#记住我

# 注册验证
class RegisterForm(forms.Form,FormMinin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={"max_length":"手机号太长","min_length":"手机号有点短", "required":'手机号不能为空'})
    password = forms.CharField(max_length=20, min_length=6, error_messages={"max_length":"密码长度有误","min_length":"密码长度太短","requierd":"密码不能为空"})
    sms_captcha = forms.CharField(max_length=4, min_length=4, error_messages={"max_length":"验证码长度有误","min_length":"验证码长度太短","required":"验证码不能为空"})
    password_repeat = forms.CharField(max_length=20, min_length=6, error_messages={"max_length": "密码长度有误", "min_length": "密码长度太短", "required": "确认密码不能为空"})
    username = forms.CharField(max_length=50,min_length=2,error_messages={"max_length":"用户名太长","min_length":"用户名有点短","required":'用户名错误'})
    graph_captcha = forms.CharField(max_length=4, min_length=4, error_messages={"max_length":"图形验证码长度有误","min_length":"图形验证码长度太短","required":"图形验证码不能为空"})


    def check_data(self):
        #判断密码是否一至
        password = self.cleaned_data.get("password")
        password_repeat = self.cleaned_data.get("password_repeat")
        if password != password_repeat:

            return self.add_error("password_repeat","两次密码不一至")

        #判断手机验证码是否一至
        sms_captcha = self.cleaned_data.get("sms_captcha")
        sms_captcha_cache = mccache.get_key(sms_captcha)
        print("*********")
        print(sms_captcha,sms_captcha_cache)
        print("*********")
        if not sms_captcha_cache and sms_captcha_cache!=sms_captcha:

            return self.add_error("sms_captcha","手机验证码错误")



        graph_captcha = self.cleaned_data.get("graph_captcha")
        graph_captcha_cache = mccache.get_key("graph_captcha")
        if not graph_captcha_cache and graph_captcha_cache != graph_captcha:
            return self.add_error("graph_captcha", "图形验证码错误")


        return True





# 重置密码验证
class VerifyForm(forms.Form, FormMinin):
    telephone = forms.CharField(max_length=11, min_length=11, error_messages={"max_length":"手机号太长","min_length":"手机号有点短","required":'手机号不能为空'})
    sms_captcha = forms.CharField(max_length=4, min_length=4, error_messages={"max_length":"验证码长度有误","min_length":"验证码长度太短","required":"验证码不能为空"})

    def verify(self):
        #判断手机验证码是否一至
        sms_captcha = self.cleaned_data.get("sms_captcha")
        sms_captcha_cache = mccache.get_key(sms_captcha)
        print("*********")
        print(sms_captcha,sms_captcha_cache)
        print("*********")
        print(sms_captcha_cache!=sms_captcha)
        if not sms_captcha_cache and sms_captcha_cache!=sms_captcha:
            return self.add_error("sms_captcha","手机验证码错误")
        return True

class PasswordForm(forms.Form,FormMinin):
    pwd = forms.CharField(max_length=20, min_length=6, error_messages={"max_length" : "密码长度有误","min_length":"密码长度太短","required":"密码不能为空"})
    rest_pwd = forms.CharField(max_length=20, min_length=6, error_messages={"max_length" : "确认密码长度有误","min_length":"确认密码长度太短", "required":"确认密码不能为空"})