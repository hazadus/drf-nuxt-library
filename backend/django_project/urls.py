"""
URL configuration for django_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _

urlpatterns = [
    path("admin/", admin.site.urls),
]

# Configure Admin panel titles
admin.site.site_header = _("Панель управления Библиотекой")
admin.site.site_title = _("Управление Библиотекой")
admin.site.index_title = _("Управление Библиотекой")
