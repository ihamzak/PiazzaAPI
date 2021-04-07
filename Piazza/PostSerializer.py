from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Post, Like
from .CommentSerializer import CommentSerializer
from .LikeSerializer import LikeSerializer


class PostSerializer(ModelSerializer):
    comment = CommentSerializer(many=True, source="comments", read_only=True)
    likes = LikeSerializer(many=True,source="like", read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
