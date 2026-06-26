"""
Token Schemas — JWT Request/Response Models

Classes:
    Token         → Response with access_token + refresh_token + token_type
    TokenPayload  → Decoded JWT payload (sub, exp, iat, type)
    RefreshTokenRequest → Request body for token refresh endpoint
"""
