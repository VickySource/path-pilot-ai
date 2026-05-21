from typing import Any, TypedDict


class CareerState(TypedDict, total=False):
    goal: str
    document_id: str | None
    context: str
    skills: list[dict]
    gaps: list[dict]
    steps: list[dict]
    critique: str
    meta: dict[str, Any]
