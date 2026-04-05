from rest_framework.generics import ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet

from apps.permissions import IsAuthorOrReadOnly
from apps.posts.models import Category, Tag, Post
from apps.posts.serializers import (
    CategorySerializer,
    TagSerializer,
    PostListSerializer,
    PostDetailSerializer,
    PostCreateUpdateSerializer,
)


class PostViewSet(ModelViewSet):
    """
    Full CRUD for Post model — list, create, retrieve, update, partial_update, destroy.

    - queryset: Post.objects.all() (for list: only published posts for anonymous,
      all posts for the author, published for other authenticated users)
    - Use PostListSerializer for list action, PostDetailSerializer for retrieve,
      PostCreateUpdateSerializer for create/update
    - permission_classes: AllowAny for list/retrieve, IsAuthenticated for create,
      IsAuthenticated + IsAuthorOrReadOnly for update/delete
    - filterset_fields: ['category', 'status', 'is_featured', 'author']
    - search_fields: ['title', 'content', 'excerpt']
    - ordering_fields: ['created_at', 'published_at', 'views_count', 'title']
    - perform_create: set author = request.user
    - retrieve: increment views_count by 1 on each GET
    """
    pass


class CategoryListCreateAPIView(ListCreateAPIView):
    """
    GET /api/v1/posts/categories/ — List all categories.
    POST /api/v1/posts/categories/ — Create a new category (Admin only).

    - queryset: Category.objects.all()
    - serializer_class: CategorySerializer
    - permission_classes: AllowAny for GET, IsAdminUser for POST
    """
    pass


class TagListCreateAPIView(ListCreateAPIView):
    """
    GET /api/v1/posts/tags/ — List all tags.
    POST /api/v1/posts/tags/ — Create a new tag (Admin only).

    - queryset: Tag.objects.all()
    - serializer_class: TagSerializer
    - permission_classes: AllowAny for GET, IsAdminUser for POST
    """
    pass


class MyPostsListAPIView(ListAPIView):
    """
    GET /api/v1/posts/my/ — List current user's posts (all statuses).

    - serializer_class: PostListSerializer
    - permission_classes: [IsAuthenticated]
    - get_queryset: filter by request.user
    """
    pass

