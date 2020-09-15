from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from api.serializers import (PostSerializer, CommentSerializer,
                             FollowSerializer, GroupSerializer)
from .models import Post, Comment, Follow, Group
from .permissions import OwnResourcePermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (OwnResourcePermission,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (OwnResourcePermission,)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        comments = Comment.objects.filter(post_id=self.kwargs.get('post_id'))
        return comments


class FollowViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (OwnResourcePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']


class GroupViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (OwnResourcePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']
