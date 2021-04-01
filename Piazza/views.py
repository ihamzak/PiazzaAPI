from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import *
from .PostSerializer import PostSerializer
from .CommentSerializer import CommentSerializer
from .LikeSerializer import LikeSerializer
from .DislikeSerializer import DislikeSerializer
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
from rest_framework.viewsets import ModelViewSet, ViewSet
from datetime import datetime
from pytz import utc
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_400_BAD_REQUEST


# {"username":"hamza","password":"hamza"}

class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def create(self, request, *args, **kwargs):
        post_data = request.data
        username = AccessToken.objects.get(token=request.GET['access_token'])
        new_post = Post.objects.create(title=post_data['title'], message=post_data['message'],
                                       expiration_time=utc.localize(
                                           datetime.strptime(post_data['expiration_time'], '%m/%d/%y %H:%M:%S')),
                                       topic=Topic.objects.get(topic_name=post_data['topic']),
                                       post_owner=username.user)
        new_post.save()
        serializer = PostSerializer(new_post)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        post_data = request.data
        username = AccessToken.objects.get(token=request.GET['access_token'])
        post = Post.objects.get(pk=pk)
        if username.user == post.post_owner:
            post.title = post_data['title']
            post.message = post_data['message']
            post.topic = Topic.objects.get(topic_name=post_data['topic'])
            post.post_owner = username.user
            post.save()
            return Response(PostSerializer(post).data)
        return Response(HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk, *args, **kwargs):
        # print(pk)
        username = AccessToken.objects.get(token=request.GET['access_token'])
        post = Post.objects.get(pk=pk)
        # print(username.user, " == ", post.post_owner)
        if username.user == post.post_owner:
            self.perform_destroy(post)
            return Response(data="Deleted successfully")
        elif username.user != post.post_owner:
            return Response(data="Operation not allowed")
        return Response(data="Something went wrong")

    # Change this method instead of getting the

    def retrieve(self, request, pk=None, *args, **kwargs):
        username = AccessToken.objects.get(token=request.GET['access_token'])
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        # return Response(len(serializer.data['liked_by']))
        # posts = Post.objects.all()
        if post.expiration_time < utc.localize(datetime.now()):
            post.is_live = False
            post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)


class CommentViewSet(ViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    queryset = Comment.objects.all()

    def list(self, request):
        comments = self.queryset
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        comment_data = request.data
        post = Post.objects.get(pk=comment_data['post'])
        username = AccessToken.objects.get(token=request.GET['access_token'])
        print(username)
        comment = Comment.objects.create(comment=comment_data['comment'], post=post, commented_by=username.user)
        comment.save()
        serializer = CommentSerializer(comment)
        return Response(serializer.data)
