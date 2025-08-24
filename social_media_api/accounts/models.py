from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    followers = models.ManyToManyField(
        'self', 
        symmetrical=False, 
        related_name='following',
        blank=True
    )

    def __str__(self):
        return self.username

    def follow(self, user):
        """Follow a user"""
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        """Unfollow a user"""
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        """Check if this user is following another user"""
        return self.following.filter(id=user.id).exists()

    def get_followers_count(self):
        """Get the number of followers"""
        return self.followers.count()

    def get_following_count(self):
        """Get the number of users this user is following"""
        return self.following.count()
