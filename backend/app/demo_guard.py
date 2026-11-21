"""CHỈ sử dụng khi public demo trên dữ liệu giả lập. Không phải xác thực."""
import os
from fastapi import Request
from fastapi.responses import JSONResponse


async def demo_read_only_guard(request: Request, call_next):
    enabled = os.getenv("DEMO_READ_ONLY", "0") == "1"
    if enabled and request.method not in {"GET", "HEAD", "OPTIONS"}:
        return JSONResponse(
            status_code=403,
            content={"detail": "Public demo: read-only mode"},
        )
    return await call_next(request)
