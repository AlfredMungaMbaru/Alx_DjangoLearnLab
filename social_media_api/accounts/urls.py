from django.urls import path
from .views import UserRegistrationView, user_login, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', user_login, name='user-login'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]
