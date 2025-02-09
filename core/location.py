import json
import requests
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import UserLocation  # Create this model to store user locations

@csrf_exempt
@login_required(login_url='/login')
def save_location(request):
    """Save user location and check if it varies from the previous one."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            latitude = data.get("latitude")
            longitude = data.get("longitude")

            if latitude is None or longitude is None:
                return JsonResponse({"success": False, "message": "Invalid location data"}, status=400)

            user = request.user
            user_location, created = UserLocation.objects.get_or_create(user=user)

            # Compare with previous location
            if not created and (user_location.latitude != latitude or user_location.longitude != longitude):
                # Send location varies alert
                requests.post("http://127.0.0.1:8001/location", json={"username": user.username})
            
            # Save new location
            user_location.latitude = latitude
            user_location.longitude = longitude
            user_location.save()

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON format"}, status=400)

    return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

