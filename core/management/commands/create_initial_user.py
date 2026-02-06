"""
Management command to create the initial user for Jayti.

This command creates the default user with:
- Username: jayati
- Password: jayati2026

Usage:
    python manage.py create_initial_user
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core.models import UserProfile


class Command(BaseCommand):
    help = 'Creates the initial user for Jayti with default credentials'

    def handle(self, *args, **kwargs):
        username = 'jayati'
        password = 'jayati2026'
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User "{username}" already exists. Skipping creation.')
            )
            return
        
        # Create the superuser
        user = User.objects.create_superuser(
            username=username,
            password=password,
            first_name='Jayti',
            last_name='Pargal',
            email='jayti@jaytipargal.in'
        )
        
        # Create user profile
        UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'display_name': 'Jayti',
                'preferred_language': 'en',
                'timezone': 'Asia/Kolkata'
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully created user "{username}" with password "{password}"')
        )
        self.stdout.write(
            self.style.SUCCESS('Jayti can change her password after first login from Profile settings.')
        )
