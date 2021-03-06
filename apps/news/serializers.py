from rest_framework import serializers
from .models import NewsComment,NewTag,News
from apps.account.serializer import UserAccountSerializer


class NewsCommentSerializers(serializers.ModelSerializer):
    author = UserAccountSerializer()
    class Meta:
        model = NewsComment
        # 序列化所有字段
        # fields = '__all__'
        # 做者是一个外键不能直接序列化
        fields = ('id', 'content', 'create_time', 'author')

class NewsTagSerializers(serializers.ModelSerializer):
    class Meta:
        model = NewTag
        fields = ('name',)

class NewsSerializers(serializers.ModelSerializer):
    author = UserAccountSerializer()
    tag = NewsTagSerializers()
    class Meta:
        model = News
        fields = ('title', 'desc', 'thumbnail_url', 'pub_time', 'author', 'tag')
