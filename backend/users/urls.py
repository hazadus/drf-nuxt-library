from django.urls import path

from .views import AuthenticatedUserDetailView

urlpatterns = [
    path("user/details/", AuthenticatedUserDetailView.as_view()),
]
