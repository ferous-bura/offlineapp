from django.contrib import admin

from core.models import OfflineUsers, License

# Register your models here.

admin.site.register(OfflineUsers)

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('owner', 'license_key', 'machine_id')
    search_fields = ('owner', 'license_key')
