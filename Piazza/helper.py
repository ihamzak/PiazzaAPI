from .models import Like, Post
import pytz
import datetime
from django.utils.timezone import localtime


class LikeUtils:
    @staticmethod
    def checkAlreadyLiked(self, post_id: Like.post_id, user: Like.liked_by):
        like_object = Like.objects.get(post_id=post_id, liked_by=user.user)
        if like_object.is_liked:
            return True
        return False

    @staticmethod
    def getLikeObject(self, post_id, user):
        like_object = Like.objects.get(post_id=post_id, liked_by=user.user)
        return like_object


def updatePostStatus():
    queryset = Post.objects.filter(is_live=True)
    for post in queryset:
        print(localtime())
        if post.expiration_time < localtime():
            post.is_live = False
            post.save()
