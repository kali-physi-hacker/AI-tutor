from __future__ import annotations

import time
from collections import defaultdict, deque
from typing import Deque, Dict

from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.responses import JSONResponse


class SimpleRateLimitMiddleware:
    def __init__(self, app: ASGIApp, limit: int = 120, window_seconds: int = 60):
        self.app = app
        self.limit = limit
        self.window = window_seconds
        self.hits: Dict[str, Deque[float]] = defaultdict(deque)

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        client = (scope.get("client") or ("", 0))[0]
        now = time.time()
        q = self.hits[client]
        q.append(now)
        while q and (now - q[0]) > self.window:
            q.popleft()
        if len(q) > self.limit:
            resp = JSONResponse({"detail": "Rate limit exceeded"}, status_code=429)
            await resp(scope, receive, send)
            return
        await self.app(scope, receive, send)

