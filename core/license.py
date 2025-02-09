from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
from .models import License

import json
import uuid
import hashlib
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .models import License

@csrf_exempt
def request_license(request):
    """Handle requests for a new license."""
    try:
        if request.method != "POST":
            return JsonResponse({"error": "Invalid request method"}, status=405)

        data = json.loads(request.body)
        username = data.get("username")
        machine_id = data.get("machine_id")

        if not username or not machine_id:
            return JsonResponse({"error": "Username and machine ID are required"}, status=400)

        try:
            user = User.objects.get(username=username)  # Ensure user exists
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found"}, status=404)

        # Check if a license already exists for this machine_id and owner
        license_obj, created = License.objects.get_or_create(machine_id=machine_id, owner=user)

        if created:
            # Generate a unique license key if it's a new record
            raw_key = f"{user.username}-{uuid.uuid4()}"
            hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()[:16].upper()

            # Ensure key is unique
            while License.objects.filter(license_key=hashed_key).exists():
                raw_key = f"{user.username}-{uuid.uuid4()}"
                hashed_key = hashlib.sha256(raw_key.encode()).hexdigest()[:16].upper()

            license_obj.license_key = hashed_key
            license_obj.save()

        return JsonResponse({"license_key": license_obj.license_key})

    except Exception as e:
        print(e)
        return JsonResponse({"error": str(e)}, status=500)

def validate_license(request, license_key, machine_id):
    """Validate license key and machine ID."""
    try:
        license_obj = License.objects.get(license_key=license_key)
        
        if license_obj.machine_id != machine_id:
            return JsonResponse({"valid": False, "error": "License already in use on another machine"})
        
        return JsonResponse({"valid": True})
    except License.DoesNotExist:
        return JsonResponse({"valid": False, "error": "Invalid license key"})
