from django.shortcuts import get_object_or_404
from posts.models import Comment, Group, Post, User
from rest_framework import status, viewsets
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


class CommentsViewSet (viewsets.ViewSet):
    def get_queryset(self):
        qs = Comment.objects.filter(post=self.kwargs['post_id'])
        return qs

    def get_object(self):
        obj = get_object_or_404(Comment, id=self.kwargs['pk'])
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, post_id, pk):
        instance = self.get_object()
        serializer = CommentSerializer(instance, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = CommentSerializer(instance,
                                       data=request.data,
                                       partial=partial
                                       )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        post_id = kwargs.pop('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer, post)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer, post):
        serializer.save(author=self.request.user,
                        post=post)

    def perform_update(self, serializer):
        if serializer.instance.author != self.request.user:
            raise PermissionDenied(ERROR_MESSAGES['OTHER_USER_DENIED'])
        if serializer.is_valid():
            serializer.save()

    def perform_destroy(self, instance):
        if instance.author != self.request.user:
            raise PermissionDenied(ERROR_MESSAGES['OTHER_USER_DENIED'])
        instance.delete()
