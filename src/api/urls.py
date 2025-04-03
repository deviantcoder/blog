from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('posts/latest/', views.LatestPostsAPIView.as_view(), name='latest_posts_api'),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view(), name='post_detail_api'),
]