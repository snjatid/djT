from rest_framework import serializers
from .models import NewsComment
from apps.account.serializer import UserAccountSerializer


class NewsCommentSerializers(serializers.ModelSerializer):
    author = UserAccountSerializer()
    class Meta:
        model = NewsComment
        # 序列化所有字段
        # fields = '__all__'
        # 做者是一个外键不能直接序列化
        fields = ('id', 'content', 'create_time', 'author')