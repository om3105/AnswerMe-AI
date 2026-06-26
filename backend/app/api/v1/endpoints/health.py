"""
Health Check Endpoints

Routes:
    GET /health          → Basic liveness probe (is the process alive?)
    GET /health/ready    → Readiness probe (can it serve traffic? checks DB + Redis)
    GET /health/detailed → Detailed system health (protected, admin-only)
"""
