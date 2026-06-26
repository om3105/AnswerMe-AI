"""
Authentication Endpoints

Routes:
    POST /auth/register  → Create a new user account
    POST /auth/login     → Authenticate and receive JWT tokens
    POST /auth/refresh   → Refresh an expired access token
    GET  /auth/me        → Get the current authenticated user's profile
"""

from fastapi import APIRouter, Depends, status

from app.api.deps import get_auth_service, get_current_user
from app.models.user import User
from app.schemas.token import RefreshTokenRequest, Token
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.services.auth_service import AuthService

router = APIRouter()


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Create a new user account with email and password.",
)
async def register(
    user_data: UserCreate,
    auth_service: AuthService = Depends(get_auth_service),
) -> UserResponse:
    """
    Register a new user.

    - Validates email format and password strength (via Pydantic schema)
    - Checks for duplicate email (via AuthService)
    - Hashes the password (via bcrypt)
    - Creates the user in the database
    - Returns the created user (without hashed_password)
    """
    user = await auth_service.register(user_data)
    return UserResponse.model_validate(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Login and get tokens",
    description="Authenticate with email and password. Returns access and refresh tokens.",
)
async def login(
    credentials: UserLogin,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """
    Authenticate a user and return JWT tokens.

    - Verifies email exists
    - Verifies password matches
    - Checks account is active
    - Returns access_token + refresh_token
    """
    return await auth_service.authenticate(
        email=credentials.email,
        password=credentials.password,
    )


@router.post(
    "/refresh",
    response_model=Token,
    summary="Refresh access token",
    description="Exchange a valid refresh token for a new access token.",
)
async def refresh_token(
    body: RefreshTokenRequest,
    auth_service: AuthService = Depends(get_auth_service),
) -> Token:
    """
    Refresh an expired access token.

    - Validates the refresh token (not expired, correct type)
    - Verifies the user still exists and is active
    - Issues a new access token
    - Returns the same refresh token (reuse until it expires)
    """
    return await auth_service.refresh_access_token(body.refresh_token)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current user",
    description="Get the profile of the currently authenticated user.",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """
    Get the current user's profile.

    Requires a valid access token in the Authorization header:
        Authorization: Bearer <access_token>

    The get_current_user dependency handles token validation
    and user lookup automatically.
    """
    return UserResponse.model_validate(current_user)
