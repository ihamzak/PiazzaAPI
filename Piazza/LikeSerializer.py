from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Like


class LikeSerializer(ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'



