#zhouzhe {Administrator}
#DATE {2018/10/9}

from django.urls import path
from .import views


app_name = 'admin_cms'
# reverse('new':index)
urlpatterns = [
    path('', views.admin, name="admin_cms"),
    path('news_tag_manage/', views.NewTagView.as_view(), name="news_tag_manage"),
    path('news_pub/', views.NewsPubView.as_view(), name="NewsPubView"),
    path('up_token/', views.up_token, name="up_token"),
    path('upload_file/', views.upload_file, name="upload_file"),
    path('news_manage/', views.News_ManageView.as_view(), name="news_manage"),

]