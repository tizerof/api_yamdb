from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailConfirmApiView, sendJWTModelViewSet, UsersModelViewSet

v1_router = DefaultRouter()

v1_router.register(
    r'users',
    UsersModelViewSet,
)

v1_router.register(
    r'auth/token',
    sendJWTModelViewSet,
)

urlpatterns = [
    path('v1/auth/email/', EmailConfirmApiView.as_view()),
    path('v1/', include(v1_router.urls))
]
