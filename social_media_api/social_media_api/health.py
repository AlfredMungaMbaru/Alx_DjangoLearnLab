from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import redis
import os


@require_http_methods(["GET"])
@csrf_exempt
def health_check(request):
    """
    Health check endpoint for monitoring and load balancers.
    Returns the health status of the application and its dependencies.
    """
    health_status = {
        "status": "healthy",
        "timestamp": None,
        "services": {
            "database": "unknown",
            "redis": "unknown"
        }
    }
    
    # Check database connectivity
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result and result[0] == 1:
                health_status["services"]["database"] = "healthy"
            else:
                health_status["services"]["database"] = "unhealthy"
                health_status["status"] = "unhealthy"
    except Exception as e:
        health_status["services"]["database"] = f"unhealthy: {str(e)}"
        health_status["status"] = "unhealthy"
    
    # Check Redis connectivity (if configured)
    try:
        redis_url = os.environ.get('REDIS_URL')
        if redis_url:
            r = redis.from_url(redis_url)
            r.ping()
            health_status["services"]["redis"] = "healthy"
        else:
            health_status["services"]["redis"] = "not_configured"
    except Exception as e:
        health_status["services"]["redis"] = f"unhealthy: {str(e)}"
        health_status["status"] = "degraded"
    
    # Set timestamp
    from datetime import datetime
    health_status["timestamp"] = datetime.now().isoformat()
    
    # Return appropriate status code
    status_code = 200 if health_status["status"] in ["healthy", "degraded"] else 503
    
    return JsonResponse(health_status, status=status_code)
