from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import hashlib

class BlockedDevice(models.Model):
    device_id = models.CharField(max_length=255, unique=True)
    ip_address = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    blocked_at = models.DateTimeField(auto_now_add=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.device_id} - {self.ip_address}"

    def is_currently_blocked(self):
        if self.blocked_until:
            return self.is_blocked and timezone.now() < self.blocked_until
        return self.is_blocked

class BlockedIP(models.Model):
    ip_address = models.CharField(max_length=255, unique=True)
    blocked_at = models.DateTimeField(auto_now_add=True)
    blocked_until = models.DateTimeField(null=True, blank=True)
    is_blocked = models.BooleanField(default=True)

    def __str__(self):
        return self.ip_address

class OfflineUsers(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name="offline")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=1000)
    credit = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_updated = models.DateTimeField(default=now)  # Track last update date
    device_id = models.CharField(max_length=255, blank=True, null=True)  # Store unique device ID
    old_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_added_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    new_user = models.BooleanField(default=True)

    def __str__(self):
        return self.owner.username

class UserLocation(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

# class UserDevice(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     device_id = models.CharField(max_length=255, unique=True)  # Unique device binding

class License(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    machine_id = models.CharField(max_length=50, unique=True)
    license_key = models.CharField(max_length=16, unique=True)

    def generate_unique_key(self):
        """Generate a unique 16-character license key."""
        while True:
            raw_key = f"{self.owner.username}-{uuid.uuid4()}" if self.owner else str(uuid.uuid4())
            hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()[:16].upper()

            # Ensure the key is unique in the database
            if not License.objects.filter(license_key=hashed_key).exists():
                return hashed_key

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = self.generate_unique_key()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.owner.username} - {self.license_key}" if self.owner else f"Unassigned - {self.license_key}"
