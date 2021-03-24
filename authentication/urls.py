from django.urls import path, include
from rest_framework.routers import DefaultRouter, Route, SimpleRouter, DynamicRoute

from .views import (sendJWTViewSet, UsersViewSet,
                    EmailConfirmationViewSet, SpecificUserViewSet, UserAPIView)


class CustomUserRouter(SimpleRouter):
    routes = [
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'delete': 'destroy',
                'patch': 'partial_update',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),
    ]


v1_router = DefaultRouter()
v1_user_router = CustomUserRouter()

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


v1_user_router.register('users', SpecificUserViewSet,
                        basename='users')

urlpatterns = [
    path('v1/users/me/', UserAPIView.as_view()),
    path('v1/', include(v1_user_router.urls)),
    path('v1/', include(v1_router.urls)),
]
