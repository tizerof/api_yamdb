from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (sendJWTModelViewSet, UsersModelViewSet,
                    EmailConfirmationViewSet)

v1_router = DefaultRouter()

v1_router.register(
    r'users',
    UsersModelViewSet,
)

v1_router.register(
    r'auth/token',
    sendJWTModelViewSet,
)

v1_router.register(
    r'auth/email',
    EmailConfirmationViewSet,
)

urlpatterns = [
    path('v1/', include(v1_router.urls))
]
