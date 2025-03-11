from django.urls import path
from . import views

app_name = 'socialaccounts'

urlpatterns = [
    path('oauth/<str:provider>/', views.oauth_login, name='oauth_login'),
    path('oauth/<str:provider>/callback/', views.oauth_callback, name='oauth_callback'),
]