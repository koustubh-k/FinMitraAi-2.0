import time
import uuid
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.logger import request_id_var, setup_logger

logger = setup_logger(__name__)

# Global rate limiter instance — shared across the application
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that generates a unique request_id for each HTTP request,
    injects it into the structured logger context, and measures total latency.
    """
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        req_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        # Set the context variable for the logger
        token = request_id_var.set(req_id)
        
        start_time = time.perf_counter()
        
        logger.info(
            "HTTP Request Started", 
            extra={"extra": {"method": request.method, "url": str(request.url)}}
        )
        
        try:
            response = await call_next(request)
            
            process_time_ms = (time.perf_counter() - start_time) * 1000
            
            # Inject request_id into response headers
            response.headers["X-Request-ID"] = req_id
            response.headers["X-Process-Time-Ms"] = str(round(process_time_ms, 2))
            
            logger.info(
                "HTTP Request Completed", 
                extra={"extra": {
                    "method": request.method, 
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "duration_ms": round(process_time_ms, 2)
                }}
            )
            return response
            
        except Exception as e:
            process_time_ms = (time.perf_counter() - start_time) * 1000
            logger.error(
                "HTTP Request Failed",
                exc_info=True,
                extra={"extra": {
                    "method": request.method, 
                    "url": str(request.url),
                    "duration_ms": round(process_time_ms, 2),
                    "error": str(e)
                }}
            )
            raise
        finally:
            request_id_var.reset(token)
