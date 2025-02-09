from decimal import Decimal
import json
import sqlite3
import time
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import now
from core.models import OfflineUsers, User, UserLocation
from django.db import transaction

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
        latitude = data.get('latitude')  # Capture latitude
        longitude = data.get('longitude')  # Capture longitude

        retries = 5
        while retries > 0:
            try:
                with transaction.atomic():
                    print(1)
                    user = get_object_or_404(User, username=username)
                    print(2)
                    offline_user = get_object_or_404(OfflineUsers, owner=user)
                    print(3)
                    is_new = offline_user.new_user
                    print(4)
                    if is_new:
                        offline_user.device_id = device_id  # Store device ID for tracking
                        offline_user.new_user = False
                    else:
                        offline_user = get_object_or_404(OfflineUsers, owner=user, device_id=device_id)
                    print(f' verify_update_balance {user}, {offline_user}')
                    added_balance = offline_user.balance
                    last_updated = user.offline.last_updated  # Ensure your model has a last_updated field
                    today = now().date()

                    # Prevent adding if requested on the same date
                    if offline_user.balance == 0:
                        return JsonResponse({"success": False, "message": "Contact Master Please.", "new_balance": str(offline_user.last_added_balance)})

                    # Prevent adding if requested on the same date
                    if last_updated and last_updated.date() == today:
                        return JsonResponse({"success": False, "message": "Balance already updated today.",  "new_balance": str(offline_user.last_added_balance)})

                    # If balance is greater than 2000, return "Finish first"
                    if old_balance > 10000:
                        return JsonResponse({"success": False, "message": "Finish first."})

                    # Update user location
                    if latitude is not None and longitude is not None:
                        user_location, created = UserLocation.objects.get_or_create(user=user)
                        user_location.latitude = latitude
                        user_location.longitude = longitude
                        user_location.save()

                    offline_user.last_updated = now()
                    offline_user.old_balance = old_balance  # Store device ID for tracking
                    offline_user.last_added_balance = added_balance
                    offline_user.balance = 0
                    offline_user.save()
                    return JsonResponse({"success": True, "message": "Balance updated successfully.", "new_balance": str(added_balance)})

            except User.DoesNotExist:
                print(f'user error ')
                return JsonResponse({"success": False, "message": f"Error: No User Found"}, status=404)

            except OfflineUsers.DoesNotExist as e:
                print(f'offline user error {e}')
                return JsonResponse({"success": False, "message": f"Error: User Not Registered"}, status=404)

            except sqlite3.OperationalError:
                retries -= 1
                if retries == 0:
                    return JsonResponse({"success": False, "message": "Database is locked, please try again later."}, status=500)
                time.sleep(1)  # Wait for a short period before retrying

    except json.JSONDecodeError:
        return JsonResponse({"success": False, "message": "Invalid JSON format."}, status=400)

    except Exception as e:
        print(f'error {e}')
        return JsonResponse({"success": False, "message": f"Error: Call Master"}, status=500)
