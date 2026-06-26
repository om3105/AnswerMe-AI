"""
User Schemas — Request/Response Models

Classes:
    UserCreate    → POST /auth/register request body
    UserLogin     → POST /auth/login request body
    UserResponse  → User data returned in API responses
    UserInDB      → Internal model (includes hashed_password)
    UserUpdate    → PATCH /users/{id} request body (all fields optional)
"""
