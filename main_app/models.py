from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from datetime import datetime

class StreamUser(AbstractUser):
    """
    Extended user model to store Stream-specific user information.
    Inherits from Django's AbstractUser for basic user functionality.
    """
    stream_user_id = models.CharField(max_length=255, unique=True)
    image = models.URLField(max_length=500, blank=True)
    last_active = models.DateTimeField(default=timezone.now)
    stream_role = models.CharField(max_length=50, default='user')
    
    # Override the groups field with a unique related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='stream_user_set',
        related_query_name='stream_user'
    )
    
    # Override the user_permissions field with a unique related_name
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='stream_user_set',
        related_query_name='stream_user'
    )
    
    class Meta:
        db_table = 'main_app_streamuser'  # Changed to match Django's naming convention
        indexes = [
            models.Index(fields=['stream_user_id']),
            models.Index(fields=['email']),
        ]

    def __str__(self):
        return f"{self.email} ({self.stream_user_id})"

    def update_last_active(self):
        """Update the last active timestamp for the user."""
        self.last_active = timezone.now()
        self.save(update_fields=['last_active'])

class StreamToken(models.Model):
    """
    Model to store Stream API tokens and their metadata.
    """
    user = models.ForeignKey(
        StreamUser,
        on_delete=models.CASCADE,
        related_name='stream_tokens'
    )
    token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'main_app_streamtoken'  # Changed to match Django's naming convention
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"Token for {self.user.email} (expires: {self.expires_at})"

    @property
    def is_expired(self):
        """Check if the token has expired."""
        return timezone.now() > self.expires_at

    def invalidate(self):
        """Mark the token as inactive."""
        self.is_active = False
        self.save(update_fields=['is_active'])

class StreamUserCustomData(models.Model):
    """
    Model to store additional custom data for Stream users.
    """
    user = models.OneToOneField(
        StreamUser,
        on_delete=models.CASCADE,
        related_name='custom_data'
    )
    custom_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'main_app_streamusercustomdata'  # Changed to match Django's naming convention

    def __str__(self):
        return f"Custom data for {self.user.email}"

    def update_custom_data(self, new_data):
        """Update custom data, maintaining creation timestamp."""
        if 'created_at' not in new_data and 'created_at' in self.custom_data:
            new_data['created_at'] = self.custom_data['created_at']
        self.custom_data = new_data
        self.save()