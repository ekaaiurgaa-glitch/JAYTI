"""
URL configuration for jaytipargal project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('notes/', include('notes.urls')),
    path('diary/', include('diary.urls')),
    path('goals/', include('goals.urls')),
    path('astro/', include('astro.urls')),
    path('ai-chat/', include('ai_chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
