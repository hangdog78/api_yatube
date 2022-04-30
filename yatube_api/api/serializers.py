import sys

from posts.models import Comment, Group, Post, User
from rest_framework import serializers

sys.path.append("..")


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'posts')
        ref_name = 'ReadOnlyUsers'


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('__all__')


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = Post
        fields = ('__all__')
        read_only_fields = ('author', 'group')


class CommentSerializer (serializers.ModelSerializer):
    author = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = ('__all__')
        read_only_fields = ('author', 'post')
