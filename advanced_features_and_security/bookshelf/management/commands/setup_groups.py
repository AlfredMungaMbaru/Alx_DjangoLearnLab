from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from bookshelf.models import Book


class Command(BaseCommand):
    help = 'Create user groups and assign permissions for the bookshelf app'

    def handle(self, *args, **options):
        # Get the content type for the Book model
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Get or create custom permissions
        permissions = {}
        permission_codenames = ['can_view', 'can_create', 'can_edit', 'can_delete']
        
        for codename in permission_codenames:
            permission, created = Permission.objects.get_or_create(
                codename=codename,
                content_type=book_content_type,
                defaults={'name': f'Can {codename.split("_")[1]} book'}
            )
            permissions[codename] = permission
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created permission: {permission.name}')
                )
            else:
                self.stdout.write(f'Permission already exists: {permission.name}')

        # Create groups and assign permissions
        groups_config = {
            'Viewers': ['can_view'],
            'Editors': ['can_view', 'can_create', 'can_edit'],
            'Admins': ['can_view', 'can_create', 'can_edit', 'can_delete'],
        }

        for group_name, permission_codenames in groups_config.items():
            group, created = Group.objects.get_or_create(name=group_name)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group_name}')
                )
            else:
                self.stdout.write(f'Group already exists: {group_name}')

            # Assign permissions to the group
            for codename in permission_codenames:
                if codename in permissions:
                    group.permissions.add(permissions[codename])
            
            # Display group permissions
            group_permissions = list(group.permissions.values_list('name', flat=True))
            self.stdout.write(f'  Permissions for {group_name}: {", ".join(group_permissions)}')

        self.stdout.write(
            self.style.SUCCESS('\nGroups and permissions setup completed!')
        )
        
        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write('PERMISSIONS AND GROUPS SUMMARY')
        self.stdout.write('='*50)
        
        for group_name in groups_config.keys():
            try:
                group = Group.objects.get(name=group_name)
                permissions_list = list(group.permissions.values_list('name', flat=True))
                self.stdout.write(f'\n{group_name}:')
                for perm in permissions_list:
                    self.stdout.write(f'  - {perm}')
            except Group.DoesNotExist:
                pass
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write('Usage Instructions:')
        self.stdout.write('='*50)
        self.stdout.write('1. Go to Django Admin (/admin/)')
        self.stdout.write('2. Navigate to Authentication and Authorization > Users')
        self.stdout.write('3. Edit a user and assign them to one of the groups:')
        self.stdout.write('   - Viewers: Can only view books')
        self.stdout.write('   - Editors: Can view, create, and edit books')
        self.stdout.write('   - Admins: Can view, create, edit, and delete books')
        self.stdout.write('4. Test the permissions by logging in as different users')
        self.stdout.write('='*50)
