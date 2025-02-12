class RequestValidator:
    @staticmethod
    def validate_required_fields(request, required_fields):
        missing_fields = [field for field in required_fields if field not in request.GET]
        if missing_fields:
            return False, f"Missing required fields: {', '.join(missing_fields)}"
        return True, None


class AuthenticationHelper:
    @staticmethod
    def authenticate_request(request):
        token = request.headers.get('Authorization')
        if not token or not AuthenticationHelper.verify_token(token):
            return False, "Invalid or missing authentication token"
        return True, None

    @staticmethod
    def verify_token(token):
        # Dummy token verification logic
        return token == "valid_token"
