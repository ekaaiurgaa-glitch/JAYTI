from django.db import models
from django.contrib.auth.models import User
import uuid


class Tag(models.Model):
    """Tags for organizing notes"""
    name = models.CharField(max_length=50, unique=True)
    color = models.CharField(max_length=7, default='#F4C2C2')
    
    def __str__(self):
        return self.name


class Note(models.Model):
    """User notes with rich content"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(blank=True)  # HTML content
    content_plain = models.TextField(blank=True)  # Plain text for search
    tags = models.ManyToManyField(Tag, blank=True, related_name='notes')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_pinned = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-is_pinned', '-modified_at']
        indexes = [
            models.Index(fields=['user', '-modified_at']),
            models.Index(fields=['title']),
        ]
    
    def __str__(self):
        return self.title or f"Note {self.created_at.strftime('%Y-%m-%d')}"
    
    def save(self, *args, **kwargs):
        # Generate plain text for search
        import re
        from html import unescape
        if self.content:
            # Remove HTML tags
            plain = re.sub(r'<[^>]+>', '', self.content)
            # Unescape HTML entities
            plain = unescape(plain)
            self.content_plain = plain
        super().save(*args, **kwargs)
