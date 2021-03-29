from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import EmailConfirmationViewSet, UsersViewSet, sendJWTViewSet

v1_router = DefaultRouter()

v1_router.register(
    r'users',
    UsersViewSet,
    basename='username'
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
