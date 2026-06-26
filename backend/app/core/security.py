"""
Security — JWT Tokens & Password Hashing

This module handles all authentication cryptography:

    Password Hashing:
        - bcrypt via passlib (adaptive cost factor)
        - verify_password(plain, hashed) → bool
        - hash_password(plain) → str

    JWT Tokens:
        - create_access_token(data, expires) → str
        - create_refresh_token(data, expires) → str
        - decode_token(token) → payload dict

Security decisions:
    - bcrypt, not SHA-256: bcrypt is intentionally slow (cost factor)
      making brute-force attacks computationally expensive
    - Access tokens: short-lived (30 min), used for API calls
    - Refresh tokens: long-lived (7 days), used only to get new access tokens
    - JWT_SECRET_KEY: must be cryptographically random, never committed to Git
"""
