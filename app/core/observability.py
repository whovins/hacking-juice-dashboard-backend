from fastapi import FastAPI
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor


from .config import Settings


def configure_tracing(app: FastAPI, settings: Settings) -> None:
    if not settings.OTEL_EXPORTER_OTLP_ENDPOINT:
        return
    resource = Resource(attributes={SERVICE_NAME: "threat-intel-api"})
    provider = TracerProvider(resource=resource)
    span_exporter = OTLPSpanExporter(endpoint=settings.OTEL_EXPORTER_OTLP_ENDPOINT, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(span_exporter))
    trace.set_tracer_provider(provider)