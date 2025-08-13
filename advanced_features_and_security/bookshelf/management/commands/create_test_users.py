from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from accounts.models import CustomUser
from bookshelf.models import Book
from datetime import date


class Command(BaseCommand):
    help = 'Create test users and demonstrate permissions functionality'

    def handle(self, *args, **options):
        self.stdout.write('Creating test users for permissions demonstration...')
        
        # Create test users
        users_data = [
            ('viewer_user', 'viewer@example.com', 'Viewers'),
            ('editor_user', 'editor@example.com', 'Editors'),
            ('admin_user', 'admin@example.com', 'Admins'),
        ]
        
        for username, email, group_name in users_data:
            # Create user if doesn't exist
            user, created = CustomUser.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': username.replace('_', ' ').title(),
                    'is_active': True
                }
            )
            
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            else:
                self.stdout.write(f'User already exists: {username}')
            
            # Assign to group
            try:
                group = Group.objects.get(name=group_name)
                user.groups.add(group)
                self.stdout.write(f'  Added to group: {group_name}')
            except Group.DoesNotExist:
                self.stdout.write(f'  Warning: Group {group_name} does not exist. Run setup_groups first.')
        
        # Create sample books
        self.stdout.write('\nCreating sample books...')
        
        sample_books = [
            {
                'title': 'Django for Beginners',
                'author': 'William S. Vincent',
                'isbn': '1234567890123',
                'publication_date': date(2022, 1, 15)
            },
            {
                'title': 'Python Crash Course',
                'author': 'Eric Matthes',
                'isbn': '2345678901234',
                'publication_date': date(2021, 11, 10)
            },
            {
                'title': 'Web Development with Django',
                'author': 'Ben Shaw',
                'isbn': '3456789012345',
                'publication_date': date(2023, 3, 20)
            }
        ]
        
        admin_user = CustomUser.objects.get(username='admin_user')
        
        for book_data in sample_books:
            book, created = Book.objects.get_or_create(
                isbn=book_data['isbn'],
                defaults={**book_data, 'owner': admin_user}
            )
            
            if created:
                self.stdout.write(f'Created book: {book.title}')
            else:
                self.stdout.write(f'Book already exists: {book.title}')
        
        # Display testing instructions
        self.stdout.write('\n' + '='*60)
        self.stdout.write('TESTING INSTRUCTIONS')
        self.stdout.write('='*60)
        
        self.stdout.write('\n1. Start the development server:')
        self.stdout.write('   python manage.py runserver')
        
        self.stdout.write('\n2. Test user accounts created:')
        for username, email, group_name in users_data:
            self.stdout.write(f'   Username: {username} | Password: testpass123 | Group: {group_name}')
        
        self.stdout.write('\n3. Testing URLs:')
        self.stdout.write('   - Book List: http://127.0.0.1:8000/bookshelf/')
        self.stdout.write('   - Django Admin: http://127.0.0.1:8000/admin/')
        
        self.stdout.write('\n4. Test Scenarios:')
        self.stdout.write('   a) Login as viewer_user:')
        self.stdout.write('      - Should see books but no create/edit/delete buttons')
        self.stdout.write('      - Cannot access /bookshelf/book/create/')
        
        self.stdout.write('   b) Login as editor_user:')
        self.stdout.write('      - Can view, create, and edit books')
        self.stdout.write('      - Cannot delete books')
        
        self.stdout.write('   c) Login as admin_user:')
        self.stdout.write('      - Full access to all book operations')
        self.stdout.write('      - Can view, create, edit, and delete')
        
        self.stdout.write('\n5. Permission Verification:')
        self.stdout.write('   - Check the permissions listed on the book list page')
        self.stdout.write('   - Try accessing restricted URLs directly')
        self.stdout.write('   - Verify 403 Forbidden errors for unauthorized access')
        
        self.stdout.write('\n' + '='*60)
        
        # Display user permissions
        self.stdout.write('\nUSER PERMISSIONS SUMMARY:')
        self.stdout.write('='*60)
        
        for username, _, group_name in users_data:
            try:
                user = CustomUser.objects.get(username=username)
                permissions = user.get_all_permissions()
                book_permissions = [p for p in permissions if 'bookshelf' in p]
                
                self.stdout.write(f'\n{username} ({group_name}):')
                if book_permissions:
                    for perm in sorted(book_permissions):
                        self.stdout.write(f'  ✓ {perm}')
                else:
                    self.stdout.write('  No bookshelf permissions')
                    
            except CustomUser.DoesNotExist:
                self.stdout.write(f'\n{username}: User not found')
        
        self.stdout.write('\nTest setup completed successfully!')
        self.stdout.write('You can now test the permissions system by logging in with different users.')
