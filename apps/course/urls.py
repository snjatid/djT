#zhouzhe {Administrator}
#DATE {2018/10/9}

from django.urls import path
from .views import index

app_name = 'course'
# reverse('new':index)
urlpatterns = [
    path('', index, name="index"),
]