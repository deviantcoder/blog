from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import PostSerializer

from blog.models import Post


class PostDetailAPIView(APIView):
    def get(self, request, slug):
        try:
            post = Post.objects.get(slug=slug, status='published')
            serializer = PostSerializer(post, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class LatestPostsAPIView(APIView):
    def get(self, request):
        posts = Post.objects.filter(status='published').order_by('-created')[:5]
        serializer = PostSerializer(
            posts,
            many=True,
            context={'request': request},
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
