from __future__ import annotations

import os
from pathlib import Path


def project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def storage_dir() -> Path:
    p = project_root() / "storage" / "documents"
    p.mkdir(parents=True, exist_ok=True)
    return p

