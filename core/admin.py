from django.contrib import admin

from core.models import OfflineUsers, License, UserLocation, BlockedDevice, BlockedIP

admin.site.register(OfflineUsers)
admin.site.register(UserLocation)
admin.site.register(BlockedIP)
admin.site.register(BlockedDevice)

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('owner', 'license_key', 'machine_id')
    search_fields = ('owner', 'license_key')
