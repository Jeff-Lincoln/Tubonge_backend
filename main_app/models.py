from django.db import models
from django.utils import timezone

class CallRoom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    participants_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # Indicates whether the room is active
    
    def __str__(self):
        return self.name

    def add_participant(self):
        """Increase participants count."""
        self.participants_count += 1
        self.save()

    def remove_participant(self):
        """Decrease participants count and check if room should be deactivated."""
        if self.participants_count > 0:
            self.participants_count -= 1
            if self.participants_count == 0:
                self.is_active = False  # Optionally deactivate room if empty
            self.save()

    def close_room(self):
        """Close the room manually (set is_active to False)."""
        self.is_active = False
        self.save()

    class Meta:
        ordering = ['-created_at']  # Latest created rooms will appear first
