"""Standard API response envelope helpers.

All success responses should use `ok(data, meta=...)` so the frontend can
rely on a single shape: `{ "data": ..., "meta": {...} }`. Error responses
are produced by the centralized exception handlers in `utils.errors`.
"""
from __future__ import annotations

from typing import Any, TypeVar

from fastapi.responses import JSONResponse

T = TypeVar("T")


def ok(data: T, meta: dict[str, Any] | None = None, status_code: int = 200) -> JSONResponse:
    payload: dict[str, Any] = {"data": data}
    if meta is not None:
        payload["meta"] = meta
    return JSONResponse(payload, status_code=status_code)


def paginated(items: list[Any], *, total: int, page: int = 1, page_size: int = 50) -> JSONResponse:
    return ok(items, meta={"total": total, "page": page, "pageSize": page_size})
