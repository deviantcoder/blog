from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('edit/', views.edit_profile, name='edit_profile'),
    path('settings/', views.profile_settings, name='settings'),
]