from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from .models import Post, Comment, Like
from .serializers import PostSerializer, PostListSerializer, CommentSerializer, LikeSerializer
from .permissions import IsAuthorOrReadOnly

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """Get all comments for a specific post"""
        post = self.get_object()
        comments = post.comments.all()
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['post', 'author']
    search_fields = ['content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']

    def perform_create(self, serializer):
        comment = serializer.save(author=self.request.user)
        
        # Create notification for the post author (if not commenting on own post)
        if comment.post.author != self.request.user:
            from notifications.models import Notification
            Notification.objects.create(
                recipient=comment.post.author,
                actor=self.request.user,
                verb='commented on your post',
                target=comment.post
            )

    def create(self, request, *args, **kwargs):
        # Ensure post_id is provided in the request data
        if 'post' not in request.data:
            return Response(
                {'error': 'post field is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().create(request, *args, **kwargs)

class FeedView(generics.ListAPIView):
    """
    API view to retrieve the feed of posts from users that the current user follows.
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    filter_backends = [filters.OrderingFilter]
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Return posts from users that the current user follows.
        """
        user = self.request.user
        # Get users that the current user is following
        following_users = user.following.all()
        
        if following_users.exists():
            # Get posts from followed users, ordered by creation date (newest first)
            return Post.objects.filter(author__in=following_users).order_by('-created_at')
        else:
            # If not following anyone, return empty queryset
            return Post.objects.none()

    def list(self, request, *args, **kwargs):
        """
        Override list method to provide additional context
        """
        queryset = self.get_queryset()
        following_count = request.user.following.count()
        
        if following_count == 0:
            return Response({
                'message': 'You are not following anyone yet. Follow some users to see their posts in your feed.',
                'following_count': 0,
                'posts': []
            })

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                'following_count': following_count,
                'posts': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'following_count': following_count,
            'posts': serializer.data
        })


class LikeUnlikeView(generics.GenericAPIView):
    """
    API view to like or unlike a post.
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Like a post"""
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        # Check if user already liked this post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        if created:
            # Create notification for the post author (if not liking own post)
            if post.author != user:
                from notifications.models import Notification
                Notification.objects.create(
                    recipient=post.author,
                    actor=user,
                    verb='liked your post',
                    target=post
                )
            
            return Response({
                'message': 'Post liked successfully',
                'liked': True,
                'likes_count': post.likes.count()
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'message': 'You have already liked this post',
                'liked': True,
                'likes_count': post.likes.count()
            }, status=status.HTTP_200_OK)
    
    def delete(self, request, pk):
        """Unlike a post"""
        post = generics.get_object_or_404(Post, pk=pk)
        user = request.user
        
        try:
            like = Like.objects.get(user=user, post=post)
            like.delete()
            
            # Remove notification if exists
            if post.author != user:
                from notifications.models import Notification
                Notification.objects.filter(
                    recipient=post.author,
                    actor=user,
                    verb='liked your post',
                    target_content_type__model='post',
                    target_object_id=post.id
                ).delete()
            
            return Response({
                'message': 'Post unliked successfully',
                'liked': False,
                'likes_count': post.likes.count()
            }, status=status.HTTP_200_OK)
        except Like.DoesNotExist:
            return Response({
                'message': 'You have not liked this post',
                'liked': False,
                'likes_count': post.likes.count()
            }, status=status.HTTP_400_BAD_REQUEST)
