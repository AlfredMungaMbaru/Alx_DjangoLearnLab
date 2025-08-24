from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserFollowSerializer

class UserRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        # Create token for the user
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token.key,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        login(request, user)
        
        # Get token using serializer method
        token_key = serializer.get_token(user)
        
        return Response({
            'user': UserProfileSerializer(user).data,
            'token': token_key,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def follow_user(request, user_id):
    """Follow a user"""
    try:
        user_to_follow = get_object_or_404(CustomUser, id=user_id)
        
        if user_to_follow == request.user:
            return Response(
                {'error': 'You cannot follow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.user.is_following(user_to_follow):
            return Response(
                {'error': 'You are already following this user'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.follow(user_to_follow)
        
        return Response({
            'message': f'You are now following {user_to_follow.username}',
            'user': UserFollowSerializer(user_to_follow, context={'request': request}).data
        }, status=status.HTTP_200_OK)
        
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def unfollow_user(request, user_id):
    """Unfollow a user"""
    try:
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        
        if user_to_unfollow == request.user:
            return Response(
                {'error': 'You cannot unfollow yourself'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not request.user.is_following(user_to_unfollow):
            return Response(
                {'error': 'You are not following this user'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.unfollow(user_to_unfollow)
        
        return Response({
            'message': f'You have unfollowed {user_to_unfollow.username}',
            'user': UserFollowSerializer(user_to_unfollow, context={'request': request}).data
        }, status=status.HTTP_200_OK)
        
    except CustomUser.DoesNotExist:
        return Response(
            {'error': 'User not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_followers(request, user_id=None):
    """List followers of a user"""
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
    
    followers = user.followers.all()
    serializer = UserFollowSerializer(followers, many=True, context={'request': request})
    
    return Response({
        'user': user.username,
        'followers_count': followers.count(),
        'followers': serializer.data
    })

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def list_following(request, user_id=None):
    """List users that a user is following"""
    if user_id:
        user = get_object_or_404(CustomUser, id=user_id)
    else:
        user = request.user
    
    following = user.following.all()
    serializer = UserFollowSerializer(following, many=True, context={'request': request})
    
    return Response({
        'user': user.username,
        'following_count': following.count(),
        'following': serializer.data
    })
