from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_feed_view, name='home_feed'),
]