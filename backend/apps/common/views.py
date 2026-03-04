from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint for load balancers and monitoring."""
    try:
        connection.ensure_connection()
        db_status = "connected"
        http_status = 200
    except Exception:
        db_status = "disconnected"
        http_status = 503

    return Response(
        {
            "status": "ok" if http_status == 200 else "error",
            "version": "1.0.0",
            "database": db_status,
        },
        status=http_status,
    )
