from django.urls import path

from core.views import verify_update_balance


urlpatterns = [
    path("verify-update-balance/", verify_update_balance, name="verify_update_balance"),
]

