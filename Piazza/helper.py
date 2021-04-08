from .models import Like, Post
import pytz
import datetime
from django.utils.timezone import localtime

def updatePostStatus():
    queryset = Post.objects.filter(is_live=True)
    for post in queryset:
        print(localtime())
        if post.expiration_time < localtime():
            post.is_live = False
            post.save()
