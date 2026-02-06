from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """Extended user profile for Jayti"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=50, default='Jayti')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    preferred_language = models.CharField(max_length=10, default='en', choices=[
        ('en', 'English'),
        ('hi', 'हिन्दी'),
        ('he', 'Hinglish'),
    ])
    notification_enabled = models.BooleanField(default=True)
    notification_time = models.TimeField(default='09:00')
    timezone = models.CharField(max_length=50, default='Asia/Kolkata')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    
    # Birthday message display tracking
    birthday_message_seen_2026 = models.BooleanField(default=False)
    
    # Daily greeting tracking
    last_daily_greeting = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.display_name}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class DailyThought(models.Model):
    """Curated daily thoughts for login page"""
    CATEGORY_CHOICES = [
        ('resilience', 'Resilience'),
        ('growth', 'Growth'),
        ('self_compassion', 'Self-Compassion'),
        ('professional', 'Professional Excellence'),
        ('relationships', 'Relationships'),
        ('spiritual', 'Spiritual Reflection'),
    ]
    
    content = models.TextField()
    author = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.category}: {self.content[:50]}..."


class DailyFlower(models.Model):
    """Seasonal flower images for login page"""
    SEASON_CHOICES = [
        ('spring', 'Spring'),
        ('summer', 'Summer'),
        ('autumn', 'Autumn'),
        ('winter', 'Winter'),
    ]
    
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='flowers/')
    season = models.CharField(max_length=10, choices=SEASON_CHOICES)
    meaning = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
