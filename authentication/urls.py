from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailConfirmApiView, SendJWTApiView, UsersModelViewSet

v1_router = DefaultRouter()

v1_router.register(
    r'v1/users',
    UsersModelViewSet,
)

urlpatterns = [
    path('v1/auth/email/', EmailConfirmApiView.as_view()),
    path('v1/auth/token/', SendJWTApiView.as_view()),
    path('', include(v1_router.urls))
]
