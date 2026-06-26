"""
Global Exception Handlers

Catches unhandled exceptions and returns consistent, structured
JSON error responses instead of raw stack traces.

Why custom exception handlers?
    - Consistent error format across all endpoints
    - Never expose internal stack traces to clients (security)
    - Log errors with full context for debugging
    - Map exceptions to appropriate HTTP status codes
"""

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logging import get_logger

logger = get_logger(__name__)


class AppException(Exception):
    """
    Base application exception.

    All custom business exceptions should inherit from this class.
    This provides consistent error handling and logging.
    """

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: str | None = None,
    ):
        self.message = message
        self.status_code = status_code
        self.detail = detail or message
        super().__init__(self.message)


class NotFoundException(AppException):
    """Resource not found (404)."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(AppException):
    """Authentication required or failed (401)."""

    def __init__(self, message: str = "Authentication required"):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ForbiddenException(AppException):
    """Insufficient permissions (403)."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class ConflictException(AppException):
    """Resource conflict, e.g., duplicate email (409)."""

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


def register_exception_handlers(app: FastAPI) -> None:
    """
    Register all global exception handlers on the FastAPI app.

    Called once during application startup in main.py.
    """

    @app.exception_handler(AppException)
    async def app_exception_handler(
        request: Request, exc: AppException
    ) -> JSONResponse:
        """Handle all custom application exceptions."""
        request_id = getattr(request.state, "request_id", "unknown")
        logger.warning(
            "app_exception",
            request_id=request_id,
            status_code=exc.status_code,
            message=exc.message,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": True,
                "message": exc.message,
                "detail": exc.detail,
                "request_id": request_id,
            },
        )

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """Handle Pydantic validation errors (422 → 400 with clear messages)."""
        request_id = getattr(request.state, "request_id", "unknown")
        errors = exc.errors()
        logger.warning(
            "validation_error",
            request_id=request_id,
            errors=errors,
            path=request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": True,
                "message": "Validation error",
                "detail": errors,
                "request_id": request_id,
            },
        )

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """
        Catch-all for unhandled exceptions.

        NEVER expose stack traces to clients.
        Log the full error internally for debugging.
        """
        request_id = getattr(request.state, "request_id", "unknown")
        logger.error(
            "unhandled_exception",
            request_id=request_id,
            error=str(exc),
            error_type=type(exc).__name__,
            path=request.url.path,
            exc_info=True,  # Include full traceback in logs
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": True,
                "message": "Internal server error",
                "detail": "An unexpected error occurred. Please try again later.",
                "request_id": request_id,
            },
        )
