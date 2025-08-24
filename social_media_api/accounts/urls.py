from django.urls import path
from .views import (
    UserRegistrationView, user_login, UserProfileView,
    follow_user, unfollow_user, list_followers, list_following
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', user_login, name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Follow functionality
    path('follow/<int:user_id>/', follow_user, name='follow-user'),
    path('unfollow/<int:user_id>/', unfollow_user, name='unfollow-user'),
    
    # Lists
    path('followers/', list_followers, name='list-followers'),
    path('followers/<int:user_id>/', list_followers, name='list-user-followers'),
    path('following/', list_following, name='list-following'),
    path('following/<int:user_id>/', list_following, name='list-user-following'),
]
