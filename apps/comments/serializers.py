from rest_framework import serializers

from apps.comments.models import Comment, Like
from apps.users.serializers import User


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    Validates input for creating a comment.
    Model: Comment
    Fields: post, parent, content
    - author is automatically set from request.user
    - Validate that parent comment belongs to the same post (if provided)
    """

    class Meta:
        model = Comment
        fields = ['post', 'parent', 'content']

    def validate(self, data):
        parent = data.get('parent')
        post = data.get('post')

        if parent and parent.post != post:
            raise serializers.ValidationError(
                "Parent comment must belong to the same post"
            )
        return data


class CommentListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing comments.
    Model: Comment
    Fields: id, post, author (nested: id, username), parent, content,
            is_approved, replies (nested list of same serializer), created_at
    - replies = serializers.SerializerMethodField()
    - get_replies: return child comments (where parent=self)
    """
    author = CommentAuthorSerializer(read_only=True)

    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'parent', 'content',
            'is_approved', 'replies', 'created_at',
        ]

    def get_replies(self, obj):

        get_reply = obj.replies.filter(is_approved=True)
        return CommentListSerializer(get_reply, many=True).data


class CommentUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a comment (only content can be changed).
    Model: Comment
    Fields: content
    """

    class Meta:
        model = Comment
        fields = ['content']


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for liking a post.
    Model: Like
    Fields: id, post, user, created_at
    Read-only: id, user, created_at
    - user is automatically set from request.user
    - Validate that user hasn't already liked the post
    """

    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

    def validate(self, data):
        request = self.context.get('request')
        if Like.objects.filter(post=data['post'], user=request.user).exists():
            raise serializers.ValidationError("You have already liked this post.")
        return data

