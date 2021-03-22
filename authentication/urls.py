from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EmailApiView

v1_router = DefaultRouter()

urlpatterns = [
    path('email/', EmailApiView.as_view())
    ]