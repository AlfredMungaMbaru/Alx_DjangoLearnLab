from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command
import os
import sys


class Command(BaseCommand):
    help = 'Prepare the application for deployment'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-only',
            action='store_true',
            help='Only run deployment checks without making changes',
        )
        parser.add_argument(
            '--skip-static',
            action='store_true',
            help='Skip static files collection',
        )

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS('🚀 Starting deployment preparation...')
        )

        # Check deployment readiness
        self._check_deployment_readiness()

        if options['check_only']:
            self.stdout.write(
                self.style.SUCCESS('✅ Deployment checks completed')
            )
            return

        # Run migrations
        self.stdout.write('📊 Running database migrations...')
        call_command('migrate', verbosity=0)
        self.stdout.write(
            self.style.SUCCESS('✅ Migrations completed')
        )

        # Collect static files
        if not options['skip_static']:
            self.stdout.write('📁 Collecting static files...')
            call_command('collectstatic', '--noinput', verbosity=0)
            self.stdout.write(
                self.style.SUCCESS('✅ Static files collected')
            )

        # Run deployment checklist
        self.stdout.write('🔍 Running deployment checklist...')
        call_command('check', '--deploy', verbosity=0)
        self.stdout.write(
            self.style.SUCCESS('✅ Deployment checklist passed')
        )

        self.stdout.write(
            self.style.SUCCESS('🎉 Deployment preparation completed!')
        )

    def _check_deployment_readiness(self):
        """Check if the application is ready for deployment"""
        self.stdout.write('🔍 Checking deployment readiness...')

        # Check environment variables
        required_env_vars = [
            'SECRET_KEY',
            'DATABASE_URL',
        ]

        missing_vars = []
        for var in required_env_vars:
            if not os.environ.get(var):
                missing_vars.append(var)

        if missing_vars:
            self.stdout.write(
                self.style.ERROR(
                    f'❌ Missing environment variables: {", ".join(missing_vars)}'
                )
            )
            sys.exit(1)

        # Check DEBUG setting
        if settings.DEBUG:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  DEBUG is set to True. Consider setting it to False for production.'
                )
            )

        # Check ALLOWED_HOSTS
        if not settings.ALLOWED_HOSTS or settings.ALLOWED_HOSTS == ['*']:
            self.stdout.write(
                self.style.WARNING(
                    '⚠️  ALLOWED_HOSTS is not properly configured for production.'
                )
            )

        # Check SECRET_KEY
        if 'django-insecure' in settings.SECRET_KEY:
            self.stdout.write(
                self.style.ERROR(
                    '❌ SECRET_KEY appears to be using the default insecure key. '
                    'Generate a new secret key for production.'
                )
            )
            sys.exit(1)

        self.stdout.write(
            self.style.SUCCESS('✅ Basic deployment checks passed')
        )
