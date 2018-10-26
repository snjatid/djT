#zhouzhe {Administrator}
#DATE {2018/10/9}

from django.urls import path
from .import views

app_name = 'account'

urlpatterns = [
    path('login', views.LoginView.as_view(), name="login"),
    path('register', views.RegisterView.as_view(), name="register"),
    path('logout', views.logoutView, name="logout"),
    path('reset_password', views.ResetPasswordView.as_view(), name="reset_password"),
    path('update_password', views.UpdatePasswordView.as_view(), name="update_password"),
    path('graph_captcha', views.graph_captcha, name="graph_captcha"),
    path('sms_captcha', views.sms_captcha, name="sms_captcha"),

]