from django.test import TestCase
from django.contrib.auth import get_user_model
from datetime import date
from accounts.models import CustomUser

User = get_user_model()


class CustomUserModelTest(TestCase):
    """
    Test cases for the CustomUser model.
    """
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'date_of_birth': date(1990, 5, 15)
        }
    
    def test_create_user(self):
        """Test creating a regular user with custom fields."""
        user = User.objects.create_user(**self.user_data)
        
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.date_of_birth, date(1990, 5, 15))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.check_password('testpass123'))
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        admin_data = {
            'username': 'admin',
            'email': 'admin@example.com',
            'password': 'adminpass123'
        }
        
        user = User.objects.create_superuser(**admin_data)
        
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
    
    def test_age_calculation(self):
        """Test the age property calculation."""
        user = User.objects.create_user(**self.user_data)
        
        # Calculate expected age
        today = date.today()
        expected_age = today.year - 1990
        if (today.month, today.day) < (5, 15):
            expected_age -= 1
        
        self.assertEqual(user.age, expected_age)
    
    def test_age_none_when_no_birth_date(self):
        """Test age returns None when date_of_birth is not set."""
        user_data = self.user_data.copy()
        del user_data['date_of_birth']
        
        user = User.objects.create_user(**user_data)
        self.assertIsNone(user.age)
    
    def test_string_representation(self):
        """Test the string representation of the user."""
        user = User.objects.create_user(**self.user_data)
        self.assertEqual(str(user), 'testuser')
    
    def test_get_profile_photo_url_no_photo(self):
        """Test profile photo URL when no photo is uploaded."""
        user = User.objects.create_user(**self.user_data)
        expected_url = '/static/images/default-profile.png'
        self.assertEqual(user.get_profile_photo_url(), expected_url)
