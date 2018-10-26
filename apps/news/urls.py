#zhouzhe {Administrator}
#DATE {2018/10/9}

from django.urls import path
from .views import index,search
from . import views

app_name = 'news'

# reverse('new':index)
urlpatterns = [
    path('', index, name="index"),
    path('new/detail/<int:news_id>',views.news_detail, name="news_detail"),
    path('news/add-comment/',views.AddNewsCommentView.as_view(), name="news_comment"),
    path('news/comment/',views.comment_list_with_news, name="comment_list_with_news"),
    path('news/list/',views.new_list, name="news_list"),
    path('search', search, name="search"),
]