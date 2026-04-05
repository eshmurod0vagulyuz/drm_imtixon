from django.urls import path

from apps.comments.views import (
    CommentListCreateAPIView,
    CommentDetailAPIView,
    LikeToggleAPIView,
    PostLikesListAPIView,
)

app_name = 'comments'

urlpatterns = [
    path('', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('<int:pk>/', CommentDetailAPIView.as_view(), name='comment-detail'),
    path('like/', LikeToggleAPIView.as_view(), name='like-toggle'),
    path('likes/', PostLikesListAPIView.as_view(), name='post-likes'),
]

