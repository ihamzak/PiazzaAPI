from rest_framework.serializers import ModelSerializer
from .models import Post
from .CommentSerializer import CommentSerializer
from .LikeSerializer import LikeSerializer
from .DislikeSerializer import DislikeSerializer


class PostSerializer(ModelSerializer):
    comment = CommentSerializer(many=True, source="comments", read_only=True)
    liked_by = LikeSerializer(many=True, source="likes", read_only=True)
    disliked_by = DislikeSerializer(many=True, source="dislikes", read_only=True)

    class Meta:
        model = Post
        fields = '__all__'
