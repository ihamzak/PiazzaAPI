from rest_framework.serializers import ModelSerializer, SerializerMethodField
from .models import Dislike


class DislikeSerializer(ModelSerializer):

    class Meta:
        model = Dislike
        fields = '__all__'




