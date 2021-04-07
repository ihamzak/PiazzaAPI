from rest_framework.serializers import ModelSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ['comment', 'commented_by', 'created_at']
