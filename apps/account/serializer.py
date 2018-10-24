from rest_framework import serializers
from .models import User


class UserAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username')