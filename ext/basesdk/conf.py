__version__ = "0.0.1"
__pypi_username__ = "SUPERAPP"
__pypi_packagename__ = "superapprestsdk"
__github_username__ = "SUPERAPP"
__github_reponame__ = "SUPERAPP-Python-SDK"
__endpoint_map__ = {
    "live": "http://127.0.0.1:8000",
    "sandbox": "http://127.0.0.1:8000/sdk/sandbox",
}

# from django.conf import settings
# from django.core.exceptions import ImproperlyConfigured

# # Example setting with a default value
# SUPERAPP_CLIENT_ID = getattr(settings, 'SUPERAPP_CLIENT_ID', None)
# if SUPERAPP_CLIENT_ID is None:
#     raise ImproperlyConfigured("SUPERAPP_CLIENT_ID is required in settings.py.")

# # Example setting without a default value, must be set by the user
# SUPERAPP_SECRET_KEY = getattr(settings, 'SUPERAPP_SECRET_KEY', None)
# if SUPERAPP_SECRET_KEY is None:
#     raise ImproperlyConfigured("SUPERAPP_SECRET_KEY is required in settings.py.")

# # Optional setting with a default value
# SUPERAPP_MODE = getattr(settings, 'SUPERAPP_MODE', 'production')

# # Another example setting with a fallback default
# API_BASE_URL = getattr(settings, 'API_BASE_URL', '127.0.0.1:8000/')
