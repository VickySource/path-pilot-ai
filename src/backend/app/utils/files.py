import os
from pathlib import Path

from app.config import get_settings


def ensure_upload_dir() -> Path:
    p = Path(get_settings().upload_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p


def save_upload(filename: str, data: bytes) -> Path:
    base = ensure_upload_dir()
    path = base / filename
    with open(path, "wb") as f:
        f.write(data)
    return path


def file_size_mb(path: os.PathLike) -> float:
    return os.path.getsize(path) / (1024 * 1024)
