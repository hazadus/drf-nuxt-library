"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path("admin/", admin.site.urls),
    # Local apps
    path("api/v1/", include("books.urls")),
    path("api/v1/", include("users.urls")),
    # Djoser endpoints to manage users:
    path("api/v1/", include("djoser.urls")),
    path("api/v1/", include("djoser.urls.authtoken")),
    # django-debug-toolbar:
    path("__debug__/", include("debug_toolbar.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Configure Admin panel titles
admin.site.site_header = _("Панель управления Библиотекой")
admin.site.site_title = _("Управление Библиотекой")
admin.site.index_title = _("Управление Библиотекой")
