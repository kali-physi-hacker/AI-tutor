from __future__ import annotations

import logging
import os

import sentry_sdk
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from ..core.config import settings

logger = logging.getLogger(__name__)


def setup_observability() -> None:
    if settings.sentry_dsn:
        sentry_sdk.init(dsn=settings.sentry_dsn, traces_sample_rate=0.1)
        logger.info("Sentry initialized")

    endpoint = settings.otel_exporter_otlp_endpoint or os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if endpoint:
        provider = TracerProvider(resource=Resource.create({"service.name": "llm-tutor-backend"}))
        processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint))
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        logger.info("OTel exporter configured")

