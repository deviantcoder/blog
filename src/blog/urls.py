from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_feed_view, name='home_feed'),

    path('post/<str:slug>/', views.view_post, name='view_post'),
    path('create-post/', views.create_post, name='create_post'),
    path('edit-post/<str:slug>/', views.edit_post, name='edit_post'),
    path('delete-post/', views.delete_post, name='delete_post'),
]