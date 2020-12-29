"""myfundoonote URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from __future__ import absolute_import
from django.contrib import admin
from django.views.decorators.cache import cache_page
from django.urls import path, include
from rest_framework import routers
from myfundooNotes import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('',include('Label.urls')),
    path('',include('Notes.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),  
    path('login/', cache_page(40)(views.Login.as_view()), name='login'),
    path('register/', views.Registration.as_view(), name = 'register'),
    path('email-verify/', views.EmailVerification.as_view(), name="email-verify"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset-request-to-email/', views.PasswordResetRequestToEmail.as_view(),
        name="request-reset-email"),
    path('password-reset/<uidb64>/<token>/',
        views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete/', views.SetNewPasswordAPIView.as_view(),
        name='password-reset-complete'),
]