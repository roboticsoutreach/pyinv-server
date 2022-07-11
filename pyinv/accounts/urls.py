"""API URLs for accounts."""

from django.urls import path

from .views.profile import profile

urlpatterns = [
    path('profile/', profile, name='profile'),
]
