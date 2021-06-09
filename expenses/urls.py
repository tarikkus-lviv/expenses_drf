"""expenses URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from expenses.utils import views_auth
from expenses_api.routers import router as expenses_api_router
from users.routers import router as users_router

jwt_patterns = [
    path('auth/', obtain_jwt_token, name='authenticate'),
    path('refresh/', refresh_jwt_token, name='refresh'),
    path('verify/', verify_jwt_token, name='verify'),
    path('password/reset/', views_auth.PasswordResetView, name='password_reset'),
    path('password/reset/confirm/', views_auth.PasswordResetConfirmView, name='password_reset_confirm'),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(expenses_api_router.urls)),
    path('api/', include(users_router.urls)),

    path('api-token-', include(jwt_patterns)),

    path('chat/', include('notifications.urls')),
]
