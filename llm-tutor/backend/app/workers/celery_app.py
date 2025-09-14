from __future__ import annotations

from celery import Celery
from ..core.config import settings

celery_app = Celery(
    "llm_tutor",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.task_routes = {
    "app.workers.tasks.*": {"queue": "default"},
}

