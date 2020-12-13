from .models import User, post, user_rel
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = post
        fields = ['id', 'user', 'date', 'image_url', 'body', 'like_count', 'dislike_count']