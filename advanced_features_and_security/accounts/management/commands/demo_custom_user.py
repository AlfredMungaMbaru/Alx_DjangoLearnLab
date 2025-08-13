from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Demonstrate the custom user model functionality'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-demo-users',
            action='store_true',
            help='Create demonstration users',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('Custom User Model Demonstration')
        )
        self.stdout.write('=' * 50)
        
        # Display current user model information
        self.stdout.write(f"Current AUTH_USER_MODEL: {User.__module__}.{User.__name__}")
        self.stdout.write(f"User model fields: {[field.name for field in User._meta.fields]}")
        
        if options['create_demo_users']:
            self.create_demo_users()
        
        # Display existing users
        self.display_users()

    def create_demo_users(self):
        """Create demonstration users with custom fields."""
        self.stdout.write('\nCreating demonstration users...')
        
        # Create a regular user
        if not User.objects.filter(username='demo_user').exists():
            demo_user = User.objects.create_user(
                username='demo_user',
                email='demo@example.com',
                password='demo_password',
                first_name='Demo',
                last_name='User',
                date_of_birth=date(1995, 3, 20)
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created demo user: {demo_user.username}')
            )
        
        # Create an admin user
        if not User.objects.filter(username='demo_admin').exists():
            demo_admin = User.objects.create_superuser(
                username='demo_admin',
                email='admin@example.com',
                password='admin_password',
                first_name='Demo',
                last_name='Admin'
            )
            self.stdout.write(
                self.style.SUCCESS(f'Created demo admin: {demo_admin.username}')
            )

    def display_users(self):
        """Display information about existing users."""
        self.stdout.write('\nExisting users:')
        self.stdout.write('-' * 30)
        
        users = User.objects.all()
        
        if not users.exists():
            self.stdout.write('No users found. Use --create-demo-users to create some.')
            return
        
        for user in users:
            self.stdout.write(f"Username: {user.username}")
            self.stdout.write(f"  Email: {user.email}")
            self.stdout.write(f"  Full Name: {user.get_full_name() or 'Not set'}")
            self.stdout.write(f"  Date of Birth: {user.date_of_birth or 'Not set'}")
            self.stdout.write(f"  Age: {user.age or 'Not calculated'}")
            self.stdout.write(f"  Is Staff: {user.is_staff}")
            self.stdout.write(f"  Is Superuser: {user.is_superuser}")
            self.stdout.write(f"  Date Joined: {user.date_joined}")
            self.stdout.write("-" * 30)
