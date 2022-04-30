from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, User
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .serializers import (CommentSerializer,
                          GroupSerializer,
                          PostSerializer,
                          UserSerializer)
ERROR_MESSAGES = {'OTHER_USER_DENIED': 'Other user\'s content changing denied'}


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(ERROR_MESSAGES['OTHER_USER_DENIED'])
        super(PostViewSet, self).perform_update(serializer)

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(ERROR_MESSAGES['OTHER_USER_DENIED'])
        super(PostViewSet, self).perform_destroy(instance)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


@api_view(['GET', 'POST'])
def api_comments(request, post_id):
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user,
                            post_id=post_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    comments = Comment.objects.filter(post=post_id)
    serializer = CommentSerializer(comments, many=True)
    return Response(serializer.data)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def api_comments_detail(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'GET':
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    if comment.author != request.user:
        return Response(status=status.HTTP_403_FORBIDDEN)

    if request.method == 'PUT' or request.method == 'PATCH':
        serializer = CommentSerializer(comment,
                                       data=request.data,
                                       partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
