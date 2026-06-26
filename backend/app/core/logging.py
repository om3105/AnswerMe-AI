"""
Structured Logging — structlog Configuration

This module configures application-wide logging using structlog.

Why structured logging (JSON) over plain text?
    Plain text:  "2026-06-26 User 42 logged in from 192.168.1.1"
    Structured:  {"timestamp": "2026-06-26T18:00:00Z", "event": "user_login",
                  "user_id": 42, "ip": "192.168.1.1", "level": "info"}

    - Machine-parseable → works with ELK, Datadog, CloudWatch
    - Filterable → query by user_id, level, event type
    - Consistent → every log has the same shape
    - Contextual → attach request_id, user_id, trace_id to all logs in a request

Configuration strategy:
    - Development: colored console output (human-readable)
    - Production: JSON output (machine-parseable)
    - Always: request_id attached via middleware for distributed tracing
"""
