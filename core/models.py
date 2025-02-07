from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.utils import timezone

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

    def __str__(self):
        return self.owner.username
