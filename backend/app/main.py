"""
AnswerMe AI — FastAPI Application Entry Point

This module creates and configures the FastAPI application instance.
It is responsible for:
    - Creating the FastAPI app with metadata
    - Registering lifespan events (startup/shutdown)
    - Including API routers
    - Adding middleware (CORS, request ID, etc.)
    - Registering global exception handlers

Usage:
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
"""
