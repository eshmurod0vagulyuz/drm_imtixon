from rest_framework import serializers

from apps.comments.models import Comment, Like


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Validates input for creating a comment.
    Model: Comment
    Fields: post, parent, content
    - author is automatically set from request.user
    - Validate that parent comment belongs to the same post (if provided)
    """
    pass


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing comments.
    Model: Comment
    Fields: id, post, author (nested: id, username), parent, content,
            is_approved, replies (nested list of same serializer), created_at
    - replies = serializers.SerializerMethodField()
    - get_replies: return child comments (where parent=self)
    """
    pass


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a comment (only content can be changed).
    Model: Comment
    Fields: content
    """
    pass


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for liking a post.
    Model: Like
    Fields: id, post, user, created_at
    Read-only: id, user, created_at
    - user is automatically set from request.user
    - Validate that user hasn't already liked the post
    """
    pass

