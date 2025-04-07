from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
    path('posts/', views.RecentPostListAPIView.as_view()),
    path('user-posts/', views.UserPostListAPIView.as_view()),
    path('posts/<slug:slug>/', views.PostDetailAPIView.as_view()),
]