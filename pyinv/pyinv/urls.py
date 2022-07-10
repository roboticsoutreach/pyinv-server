"""
PyInv URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from assets.admin import admin_site

api_urlpatterns = [
    path('', include('assets.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='auth_token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='auth_token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='auth_token_verify'),
    path('docs/', SpectacularSwaggerView.as_view(), name='schema-docs'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]


urlpatterns = [
    path('api/v1/', include(api_urlpatterns)),
    path('admin/', admin_site.urls),
]
