from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from .models import *
from .PostSerializer import PostSerializer
from .CommentSerializer import CommentSerializer
from .LikeSerializer import LikeSerializer
# from .DislikeSerializer import DislikeSerializer
from rest_framework.response import Response
from oauth2_provider.models import AccessToken
from rest_framework.viewsets import ModelViewSet, ViewSet
from datetime import datetime
from pytz import utc, timezone
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED, HTTP_400_BAD_REQUEST
from .helper import updatePostStatus
from .DislikeSerializer import DislikeSerializer


# {"username":"hamza","password":"hamza"}


class PostViewSet(ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def list(self, request, *args, **kwargs):
        updatePostStatus()
        print(request.data)
        if 'postid' in request.data:
            q = Post.objects.filter(pk=request.data['postid'])
        else:
            q = Post.objects.all()
        serializer = PostSerializer(q, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        post_data = request.data
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip())
        new_post = Post.objects.create(title=post_data['title'], message=post_data['message'],
                                       expiration_time=timezone("Europe/London").localize(
                                           datetime.strptime(post_data['expiration_time'], '%m/%d/%y %H:%M:%S')),
                                       topic=Topic.objects.get(topic_name=post_data['topic']),
                                       post_owner=username.user)
        new_post.save()
        serializer = PostSerializer(new_post)
        return Response(serializer.data)

    def update(self, request, pk, *args, **kwargs):
        post_data = request.data
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip())
        post = Post.objects.get(pk=pk)
        if post.is_live:
            if username.user == post.post_owner:
                post.title = post_data['title']
                post.message = post_data['message']
                post.topic = Topic.objects.get(topic_name=post_data['topic'])
                post.post_owner = username.user
                post.save()
                return Response(PostSerializer(post).data)
            return Response("Post is expired now")
        return Response("Post is expired")

    def destroy(self, request, pk, *args, **kwargs):
        # print(pk)
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip())
        post = Post.objects.get(pk=pk)
        # print(username.user, " == ", post.post_owner)
        if username.user == post.post_owner:
            self.perform_destroy(post)
            return Response(data="Deleted successfully")
        elif username.user != post.post_owner:
            return Response(data="Operation not allowed")
            # return  Response("Post is expired.")
        return Response(data="OOPS something went wrong......")

    # Change this method instead of getting the

    def retrieve(self, request, pk, *args, **kwargs):
        print(request.data)
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip())
        print(username)
        post = Post.objects.get(pk=pk)
        serializer = PostSerializer(post)
        # return Response(len(serializer.data['liked_by']))
        # posts = Post.objects.all()
        if post.expiration_time < utc.localize(datetime.now()):
            post.is_live = False
            post.save()
        serializer = PostSerializer(post)
        return Response(serializer.data)


class TopicViewSet(ViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def list(self, request):
        if 'topic' not in request.data:
            return Response("Please pass in topic in request body")
        topic_data = request.data
        topic_queryset = Post.objects.filter(topic=topic_data['topic'])
        serializer = PostSerializer(topic_queryset, many=True)
        return Response(serializer.data)


class LivePostsViewSet(ViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def list(self, request):
        # check wherther the topic is present in request body if pressent then filter the posts by topic 
        if "topic" in request.data:
            live_posts_queryset = Post.objects.filter(is_live=True,topic=request.data['topic'])
            serializer = PostSerializer(live_posts_queryset, many=True)
            return Response(serializer.data)     
        live_posts_queryset = Post.objects.filter(is_live=True)
        serializer = PostSerializer(live_posts_queryset, many=True)
        return Response(serializer.data)


class ExpiredPostsViewSet(ViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def list(self, request):
                # check wherther the topic is present in request body if pressent then filter the posts by topic 
        if "topic" in request.data:
            expired_posts_queryset = Post.objects.filter(is_live=False,topic=request.data['topic'])
            serializer = PostSerializer(expired_posts_queryset, many=True)
            return Response(serializer.data) 
        expired_posts_queryset = Post.objects.filter(is_live=False)
        serializer = PostSerializer(expired_posts_queryset, many=True)
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
        print(comment_data)
        post = Post.objects.get(pk=comment_data['post'])
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip())
        print(username)
        if post.is_live:
            comment = Comment.objects.create(comment=comment_data['comment'], post=post, commented_by=username.user)
            comment.save()
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        return Response("Post is expired now ")


class LikeViewSet(ViewSet):
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Like.objects.all()

    def create(self, request):
        '''
            Like the post if the post is not already liked or disliked by the user.
        '''
        like_data = request.data # get the data from request body 
        liked_post_id = Post.objects.get(pk=like_data['liked_post_id'])  # get the post by its primary key 
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip()) # gets the user from access_token 
        if liked_post_id.is_live:
            if Like.objects.filter(liked_post_id=liked_post_id, liked_by=username.user):
                return Response("You have already like the post")

            if Dislike.objects.filter(disliked_post_id=liked_post_id, disliked_by=username.user).exists():
                return Response("You have disliked the post you can't like it anymore")
            else:
                like_object = Like.objects.create(liked_post_id=liked_post_id, liked_by=username.user)
                like_object.save()
                liked_post_id.total_likes += 1
                liked_post_id.save()
                serializer = LikeSerializer(like_object)
                return Response(serializer.data)
        return Response("Post is expired now.")


class DislikeViewSet(ViewSet):
    serializer_class = DislikeSerializer
    permission_classes = [IsAuthenticated]
    queryset = Dislike.objects.all()

    def create(self, request):
        '''
            Dislike the post if the post is not already liked or disliked by the user.
        '''
        #print(request.META['HTTP_AUTHORIZATION'])
        access_token = request.META['HTTP_AUTHORIZATION'].replace('Bearer', "").strip()
        #print(access_token)
        dislike_data = request.data
        disliked_post_id = Post.objects.get(pk=dislike_data['disliked_post_id'])
        username = AccessToken.objects.get(token=request.META['HTTP_AUTHORIZATION'].replace("Bearer", "").strip())
        if disliked_post_id.is_live:
            if Dislike.objects.filter(disliked_post_id=disliked_post_id, disliked_by=username.user).exists():
                return Response("You have already disliked the post")

            if Like.objects.filter(liked_post_id=disliked_post_id, liked_by=username.user).exists():
                return Response("You have liked the post you can't dislike it now")
            else:
                dislike_object = Dislike.objects.create(disliked_post_id=disliked_post_id, disliked_by=username.user)
                dislike_object.save()
                disliked_post_id.total_dislikes += 1
                disliked_post_id.save()
                serializer = DislikeSerializer(dislike_object)
                return Response(serializer.data)
        return Response("Post is expired now.")


from .PostSerializer import TopPostsSerializer


class TopPostsViewSet(ViewSet):
    serializer_class = TopPostsSerializer  
    permission_classes = [IsAuthenticated]
    queryset = Post.objects.all()

    def list(self, request):
        '''
            Lists top 5 posts from the queryset and shows rating , title, post_owner, topic and is_live attributes of the post. 
        '''
        query = Post.objects.extra(select={"rating": "total_likes + total_dislikes"}, order_by=['-rating','created_at']).filter(is_live=True)[:5]
        serializer = TopPostsSerializer(query, many=True)
        return Response(serializer.data)
