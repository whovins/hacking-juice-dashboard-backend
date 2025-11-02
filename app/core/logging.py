import structlog


def setup_logging(env: str = "dev") -> None:
    processors = [
    structlog.processors.TimeStamper(fmt="iso"),
    structlog.processors.add_log_level,
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.JSONRenderer(),
    ]
    structlog.configure(processors=processors)