import time
from collections import defaultdict
from app.config import RATE_LIMIT_MAX, RATE_LIMIT_WINDOW

class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()
        # Remove old requests outside the window
        self.requests[client_id] = [
            t for t in self.requests[client_id] if now - t < RATE_LIMIT_WINDOW
        ]
        if len(self.requests[client_id]) >= RATE_LIMIT_MAX:
            return False
        self.requests[client_id].append(now)
        return True

rate_limiter = RateLimiter()
