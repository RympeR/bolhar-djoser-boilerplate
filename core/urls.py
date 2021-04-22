from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from core import settings
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('rest_framework.urls')),
    path('api/user/', include('apps.users.urls')),
    path('api/chat/', include('apps.chat.urls')),
    path('silk/', include('silk.urls', namespace='silk')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)