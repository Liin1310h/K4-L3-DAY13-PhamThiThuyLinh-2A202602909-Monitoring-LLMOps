from __future__ import annotations

import time
import uuid
import re

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars


class CorrelationIdMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        clear_contextvars()
        supplied_id = request.headers.get("x-request-id", "")
        correlation_id = (
            supplied_id
            if re.fullmatch(r"req-[0-9a-fA-F]{8}", supplied_id)
            else f"req-{uuid.uuid4().hex[:8]}"
        )
        bind_contextvars(correlation_id=correlation_id)
        
        request.state.correlation_id = correlation_id
        
        start = time.perf_counter()
        response = await call_next(request)
        
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["x-request-id"] = correlation_id
        response.headers["x-response-time-ms"] = f"{elapsed_ms:.2f}"
        
        return response
