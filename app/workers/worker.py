import dramatiq
from dramatiq.brokers.redis import RedisBroker
from redis import Redis as SyncRedis
from ..core.config import get_settings


s = get_settings()
redis_broker = RedisBroker(url=s.REDIS_URL)
dramatiq.set_broker(redis_broker)


@dramatiq.actor(queue_name="maintenance")
def ping() -> None:
    # 간단한 헬스용 액터
    print("pong")


if __name__ == "__main__":
# dramatiq는 명령행 실행이 일반적이나, 데모용으로 진입점 제공
    import time
    while True:
        time.sleep(60)