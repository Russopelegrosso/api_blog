from rest_framework import viewsets, filters
from api.serializers import (PostSerializer, CommentSerializer,
                             FollowSerializer, GroupSerializer)
from .models import Post, Comment, Follow, Group
from .permissions import OwnResourcePermission


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [OwnResourcePermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        queryset = Post.objects.all()
        group_id = self.request.query_params.get('group', None)
        if group_id is not None:
            queryset = queryset.filter(group=group_id)
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [OwnResourcePermission]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        comments = Comment.objects.filter(post_id=self.kwargs.get('post_id'))
        return comments


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [OwnResourcePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [OwnResourcePermission]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']
