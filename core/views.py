from decimal import Decimal
import json
import sqlite3
import time
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from core.models import OfflineUsers, User
from django.db import transaction

BROWSER_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"

@csrf_exempt
def verify_update_balance(request):
    """Verifies and returns the user balance securely."""

    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
        username = data.get('username')
        old_balance = Decimal(data.get('old_balance'))
        device_id = data.get('device_id')
        print(f'verify_update_balance {username}, {old_balance} {device_id}')

        retries = 5
        while retries > 0:
            try:
                with transaction.atomic():
                    user = get_object_or_404(User, username=username)
                    offline_user = get_object_or_404(OfflineUsers, owner=user, device_id=device_id)
                    print(f' verify_update_balance {user}, {offline_user}')
                    added_balance = offline_user.balance
                    last_updated = user.offline.last_updated  # Ensure your model has a last_updated field
                    today = now().date()

                    # Prevent adding if requested on the same date
                    if last_updated and last_updated.date() == today:
                        return JsonResponse({"success": False, "message": "Balance already updated today."})

                    # If balance is greater than 2000, return "Finish first"
                    if old_balance > 2000:
                        return JsonResponse({"success": False, "message": "Finish first."})

                    new_balance = old_balance + added_balance
                    offline_user.last_updated = now()
                    offline_user.device_id = device_id  # Store device ID for tracking
                    offline_user.old_balance = old_balance  # Store device ID for tracking
                    offline_user.save()
                    return JsonResponse({"success": True, "message": "Balance updated successfully.", "new_balance": str(new_balance)})

            except sqlite3.OperationalError:
                retries -= 1
                if retries == 0:
                    return JsonResponse({"success": False, "message": "Database is locked, please try again later."}, status=500)
                time.sleep(1)  # Wait for a short period before retrying

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)

    except Exception as e:
        return JsonResponse({"success": False, "message": f"Error: {str(e)}"}, status=500)
