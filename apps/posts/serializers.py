from rest_framework import serializers

from apps.posts.models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes post categories.
    Model: Category
    Fields: id, name, slug, description, created_at
    Read-only: id, slug, created_at
    - slug should be auto-generated from name if not provided
    """
    pass


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes tags.
    Model: Tag
    Fields: id, name, slug
    Read-only: id, slug
    - slug should be auto-generated from name if not provided
    """
    pass


class PostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for post list views.
    Model: Post
    Fields: id, title, slug, excerpt, cover_image, status, is_featured,
            views_count, author (nested: id, username), category (nested: id, name),
            tags (nested: id, name), published_at, created_at
    - author, category, tags should display nested info (not just IDs)
    """
    pass


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for post detail view.
    Model: Post
    Fields: all fields from PostListSerializer + content + updated_at
    - author, category, tags should display nested info
    """
    pass


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Validates input for post creation and update.
    Model: Post
    Fields: title, content, excerpt, cover_image, category, tags, status, is_featured
    - author is automatically set from request.user (not in input)
    - slug auto-generated from title
    - If status changes to 'published' and published_at is null, set published_at = now
    """
    pass

