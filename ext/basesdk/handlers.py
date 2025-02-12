class BaseHandler:
    def __init__(self, request):
        self.request = request

    def validate_request(self):
        raise NotImplementedError("Subclasses must implement validate_request method")

    def process(self):
        # General processing logic
        if self.validate_request():
            return self.handle()
        else:
            return self.error_response("Invalid request", 400)

    def error_response(self, message, status):
        return {
            'status': status,
            'message': message,
        }

    def handle(self):
        raise NotImplementedError("Subclasses must implement handle method")


class ResourceHandler(BaseHandler):
    def validate_request(self):
        # Validate the request (e.g., check required fields)
        return 'data' in self.request.GET

    def handle(self):
        # Process the request and return a response
        data = self.request.GET.get('data')
        return {
            'status': 200,
            'message': 'Resource handled successfully',
            'data': data
        }


class AnotherResourceHandler(BaseHandler):
    def validate_request(self):
        # Different validation logic
        return 'id' in self.request.GET

    def handle(self):
        # Process the request and return a response
        resource_id = self.request.GET.get('id')
        return {
            'status': 200,
            'message': 'Another resource handled successfully',
            'id': resource_id
        }
