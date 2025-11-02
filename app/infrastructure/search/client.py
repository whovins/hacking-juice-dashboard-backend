from opensearchpy import OpenSearch
from ...core.config import get_settings


_settings = get_settings()
os = OpenSearch(_settings.OS_URL)


def health() -> bool:
    try:
        return os.ping()
    except Exception:
        return False