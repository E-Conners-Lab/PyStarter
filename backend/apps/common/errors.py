"""API errors omit exception text and correlate sanitized server events."""
import logging
from rest_framework.response import Response
from rest_framework.views import exception_handler

logger = logging.getLogger(__name__)


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)
    request_id = getattr(context.get('request'), 'correlation_id', 'unavailable')
    if response is None:
        logger.error('api_failure request_id=%s exception_type=%s', request_id, type(exc).__name__)
        return Response({'error': 'The request could not be completed.', 'request_id': request_id}, status=500)
    if isinstance(response.data, dict):
        response.data = {**response.data, 'request_id': request_id}
    return response
