from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.posts.views import (
    PostViewSet,
    CategoryListCreateAPIView,
    TagListCreateAPIView,
    MyPostsListAPIView,
)

app_name = 'posts'

router = DefaultRouter()
router.register('', PostViewSet, basename='post')

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('tags/', TagListCreateAPIView.as_view(), name='tag-list-create'),
    path('my/', MyPostsListAPIView.as_view(), name='my-posts'),
    path('', include(router.urls)),
]

