from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    static(settings.MEDIA_URL, documents_root=settings.MEDIA_ROOT)
