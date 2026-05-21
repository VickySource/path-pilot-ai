import time
import uuid

from fastapi import FastAPI, Request

from app.utils.logger import get_logger

logger = get_logger("http")


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def request_context(request: Request, call_next):
        request_id = request.headers.get("x-request-id", str(uuid.uuid4()))
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        response.headers["x-request-id"] = request_id
        response.headers["x-response-time-ms"] = f"{elapsed_ms:.2f}"
        logger.info(
            "%s %s -> %s in %.2fms [%s]",
            request.method, request.url.path, response.status_code, elapsed_ms, request_id,
        )
        return response
