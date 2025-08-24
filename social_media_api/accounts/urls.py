from django.urls import path
from .views import (
    UserRegistrationView, user_login, UserProfileView,
    FollowUserView, UnfollowUserView, ListFollowersView, ListFollowingView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', user_login, name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Follow functionality
    path('follow/<int:user_id>/', FollowUserView.as_view(), name='follow-user'),
    path('unfollow/<int:user_id>/', UnfollowUserView.as_view(), name='unfollow-user'),
    
    # Lists
    path('followers/', ListFollowersView.as_view(), name='list-followers'),
    path('followers/<int:user_id>/', ListFollowersView.as_view(), name='list-user-followers'),
    path('following/', ListFollowingView.as_view(), name='list-following'),
    path('following/<int:user_id>/', ListFollowingView.as_view(), name='list-user-following'),
]
