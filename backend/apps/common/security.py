"""HTTP security boundaries shared by versioned API routes."""
import uuid
from django.http import JsonResponse

SAFE_METHODS = frozenset({'GET', 'HEAD', 'OPTIONS'})


class APISecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.correlation_id = uuid.uuid4().hex
        response = self._validate(request)
        if response is None:
            response = self.get_response(request)
        if request.path.startswith('/api/'):
            response['Cache-Control'] = 'no-store'
            response['X-API-Version'] = '1'
            response['X-Request-ID'] = request.correlation_id
            response['X-Content-Type-Options'] = 'nosniff'
        return response

    def _validate(self, request):
        if not request.path.startswith('/api/') or request.method in SAFE_METHODS:
            return None
        if request.headers.get('Sec-Fetch-Site') == 'cross-site':
            return self._error(request, 'Cross-site requests are not permitted.', 403)
        if request.content_type != 'application/json':
            return self._error(request, 'Content-Type must be application/json.', 415)
        return None

    @staticmethod
    def _error(request, message, code):
        return JsonResponse({'error': message, 'request_id': request.correlation_id}, status=code)
