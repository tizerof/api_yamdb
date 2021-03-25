from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CommentViewSet, ReviewViewSet, CategoryViewSet

router = DefaultRouter()


router.register(
    r'^titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='comment')
router.register(r'categories', CategoryViewSet, basename='category'
)


urlpatterns = [
    path('v1/', include(router.urls)),
]
