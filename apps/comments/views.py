from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    GenericAPIView,
    ListAPIView,
)
from rest_framework.permissions import AllowAny, IsAuthenticated

from apps.permissions import IsAuthorOrReadOnly
from apps.comments.models import Comment, Like
from apps.comments.serializers import (
    CommentCreateSerializer,
    CommentListSerializer,
    CommentUpdateSerializer,
    LikeSerializer,
)


class CommentListCreateAPIView(ListCreateAPIView):
    """
    GET /api/v1/comments/?post=<id> — List comments for a post (top-level only, with nested replies).
    POST /api/v1/comments/ — Create a new comment.

    - serializer: CommentListSerializer for GET, CommentCreateSerializer for POST
    - permission_classes: AllowAny for GET, IsAuthenticated for POST
    - perform_create: set author = request.user
    - get_queryset: filter by post query param, only top-level (parent=None), only approved
    - filterset_fields: ['post']
    """
    pass


class CommentDetailAPIView(RetrieveUpdateDestroyAPIView):
    """
    GET /api/v1/comments/<pk>/ — Retrieve a comment.
    PUT/PATCH /api/v1/comments/<pk>/ — Update a comment (author only).
    DELETE /api/v1/comments/<pk>/ — Delete a comment (author only).

    - serializer: CommentUpdateSerializer for PUT/PATCH, CommentListSerializer for GET
    - permission_classes: IsAuthenticated, IsAuthorOrReadOnly
    """
    pass


class LikeToggleAPIView(GenericAPIView):
    """
    POST /api/v1/comments/like/ — Toggle like on a post.
    - If user already liked the post → unlike (delete the Like), return {"status": "unliked"}
    - If user hasn't liked the post → like (create the Like), return {"status": "liked"}

    - serializer_class: LikeSerializer
    - permission_classes: [IsAuthenticated]
    - Accepts: {"post": <post_id>}
    """
    pass


class PostLikesListAPIView(ListAPIView):
    """
    GET /api/v1/comments/likes/?post=<id> — List all likes for a post.

    - serializer_class: LikeSerializer
    - permission_classes: [AllowAny]
    - filterset_fields: ['post']
    """
    pass

