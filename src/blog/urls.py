from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_feed_view, name='home_feed'),

    path('post/<str:slug>/', views.view_post, name='view_post'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:slug>/', views.edit_post, name='edit_post'),
    path('delete-post/<str:slug>/', views.delete_post, name='delete_post'),
    
    path('search/', views.search, name='search'),

    path('create-comment/<str:slug>/', views.create_comment, name='create_comment'),

    path('upvote/<str:slug>/', views.upvote_post, name='upvote_post'),
]