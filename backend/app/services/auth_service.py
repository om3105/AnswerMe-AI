"""
Authentication Service — Business Logic

Responsibilities:
    - register_user(user_data) → Create account, hash password, return user
    - authenticate_user(email, password) → Verify credentials, return tokens
    - refresh_access_token(refresh_token) → Validate refresh, issue new access
    - get_current_user(token) → Decode JWT, fetch user from DB

Business rules enforced here (NOT in routes or repositories):
    - Email uniqueness validation
    - Password strength requirements
    - Account activation status check
    - Token expiration and type validation
"""
