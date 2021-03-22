from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailApiView, SendJWTApiView

v1_router = DefaultRouter()

urlpatterns = [
    path('v1/auth/email/', EmailApiView.as_view()),
    path('v1/auth/token/', SendJWTApiView.as_view())
    ]