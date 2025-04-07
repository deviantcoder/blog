from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .serializers import PostSerializer

from blog.models import Post


class RecentPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()[:2]
    serializer_class = PostSerializer


class UserPostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(author=self.request.user.profile)


class PostDetailAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.select_related('author__user').prefetch_related('tags')
    serializer_class = PostSerializer
    lookup_field = 'slug'