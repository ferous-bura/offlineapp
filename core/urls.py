from django.urls import path

from core.views import verify_update_balance
from core.license import request_license, validate_license


urlpatterns = [
    path("verify-update-balance/", verify_update_balance, name="verify_update_balance"),
    path("license-request/", request_license, name="request_license"),
    path("validate/<str:license_key>/<str:machine_id>/", validate_license, name="validate_license"),
]