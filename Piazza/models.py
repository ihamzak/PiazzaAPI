from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import pytz
import time


class Topic(models.Model):
    topic_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.topic_name


class Post(models.Model):
    title = models.CharField(max_length=350)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, to_field="topic_name")
    created_at = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
    expiration_time = models.DateTimeField()
    post_owner = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    is_live = models.BooleanField(default=True, editable=False)
    total_likes = models.IntegerField(default=0, editable=True)
    total_dislikes = models.IntegerField(default=0, editable=True)
    total_time_remaining = models.DurationField()

    def save(self, *args, **kwargs):
        if self.expiration_time >= timezone.localtime():  # pytz.utc.localize(datetime.datetime.now()):
            self.is_live = True
        else:
            self.is_live = False
        self.total_time_remaining = self.expiration_time - timezone.localtime()
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Comment(models.Model):
    comment = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    commented_by = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment


class Like(models.Model):
    liked_post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='like')
    liked_by = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)

    def __str__(self):
        return "Post: " + str(self.liked_post_id) + ", Liked by:" + str(self.liked_by)

    class Meta:
        unique_together = ('liked_post_id', 'liked_by')


class Dislike(models.Model):
    disliked_post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='dislike')
    disliked_by = models.ForeignKey(User, to_field='username', on_delete=models.CASCADE)

    def __str__(self):
        return "Post: " + str(self.disliked_post_id) + ", disiked by:" + str(self.disliked_by)

    class Meta:
        unique_together = ('disliked_post_id', 'disliked_by')
