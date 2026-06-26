"""
Request ID Middleware

Generates a unique request ID for every incoming request and attaches
it to the response headers and log context. This enables distributed
tracing — you can follow a single request across all services and logs.

How it works:
    1. Client sends request (optionally with X-Request-ID header)
    2. Middleware generates or uses the provided request ID
    3. Request ID is bound to structlog context (all logs include it)
    4. Request ID is returned in the X-Request-ID response header
    5. On request completion, the context is cleared
"""

import time
import uuid

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import get_logger

logger = get_logger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware that adds a unique request ID to every request.

    The request ID is:
        - Generated as a UUID4 (or taken from X-Request-ID header)
        - Added to the response as X-Request-ID header
        - Bound to structlog for all logs during the request
        - Used for distributed tracing and debugging
    """

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        # Use existing request ID or generate a new one
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Store in request state for access in route handlers
        request.state.request_id = request_id

        # Measure request duration
        start_time = time.monotonic()

        # Log the incoming request
        logger.info(
            "request_started",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            client_ip=request.client.host if request.client else "unknown",
        )

        # Process the request
        response = await call_next(request)

        # Calculate duration
        duration_ms = round((time.monotonic() - start_time) * 1000, 2)

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id

        # Log the completed request
        logger.info(
            "request_completed",
            request_id=request_id,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=duration_ms,
        )

        return response
