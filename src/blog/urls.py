from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.posts_list, name='posts_list'), #home_feed

    path('post/<str:slug>/', views.post_detail, name='post_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:slug>/', views.edit_post, name='edit_post'),
    path('delete-post/<str:slug>/', views.delete_post, name='delete_post'),

    path('create-comment/<str:slug>/', views.create_comment, name='create_comment'),
    path('upvote/<str:slug>/', views.upvote_post, name='upvote_post'),
    
    path('search/', views.search, name='search'),

    path('settings/', views.user_settings, name='settings'),
    path('publish-draft/', views.publish_draft, name='publish_draft'),

    path('tags/search/', views.tag_search, name='tag_search'),
]