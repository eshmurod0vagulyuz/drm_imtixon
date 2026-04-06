from datetime import timezone

from django.template.defaultfilters import slugify
from rest_framework import serializers

from apps.posts.models import Category, Tag, Post
from apps.users.serializers import User


class AuthorShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializes post categories.
    Model: Category
    Fields: id, name, slug, description, created_at
    Read-only: id, slug, created_at
    - slug should be auto-generated from name if not provided
    """

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        read_only_fields = ['id', 'slug', 'created_at']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class TagSerializer(serializers.ModelSerializer):
    """
    Serializes tags.
    Model: Tag
    Fields: id, name, slug
    Read-only: id, slug
    - slug should be auto-generated from name if not provided
    """

    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
        read_only_fields = ['id', 'slug']

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for post list views.
    Model: Post
    Fields: id, title, slug, excerpt, cover_image, status, is_featured,
            views_count, author (nested: id, username), category (nested: id, name),
            tags (nested: id, name), published_at, created_at
    - author, category, tags should display nested info (not just IDs)
    """
    author = AuthorShortSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'excerpt', 'cover_image',
            'status', 'is_featured', 'views_count',
            'author', 'category', 'tags',
            'published_at', 'created_at',
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """
    Full serializer for post detail view.
    Model: Post
    Fields: all fields from PostListSerializer + content + updated_at
    - author, category, tags should display nested info
    """
    author = AuthorShortSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt', 'cover_image',
            'status', 'is_featured', 'views_count',
            'author', 'category', 'tags',
            'published_at', 'created_at', 'updated_at',
        ]


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Validates input for post creation and update.
    Model: Post
    Fields: title, content, excerpt, cover_image, category, tags, status, is_featured
    - author is automatically set from request.user (not in input)
    - slug auto-generated from title
    - If status changes to 'published' and published_at is null, set published_at = now
    """

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'excerpt', 'cover_image',
            'category', 'tags', 'status', 'is_featured',
        ]

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])

        validated_data['slug'] = slugify(validated_data['title'])

        if validated_data.get('status') == 'published':
            validated_data['published_at'] = timezone.now()

        post = Post.objects.create(**validated_data)

        post.tags.set(tags)
        return post

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)

        if 'title' in validated_data:
            validated_data['slug'] = slugify(validated_data['title'])

        if validated_data.get('status') == 'published' and not instance.published_at:
            validated_data['published_at'] = timezone.now()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if tags is not None:
            instance.tags.set(tags)

        return instance

