from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (sendJWTViewSet, UsersViewSet,
                    EmailConfirmationViewSet)


v1_router = DefaultRouter()

v1_router.register(
    r'users',
    UsersViewSet,
)

v1_router.register(
    r'auth/token',
    sendJWTViewSet,
)

v1_router.register(
    r'auth/email',
    EmailConfirmationViewSet,
)


urlpatterns = [
    path('', include(v1_router.urls)),
]

