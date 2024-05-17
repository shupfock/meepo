import asyncio

from celery import Celery
from celery.schedules import crontab
from celery.signals import worker_process_init
from kombu import Exchange, Queue

from app.utils.logger import get_logger
from settings import config

logger = get_logger()


DEFAULT_EXCHANGE = Exchange(name="meepo", type="topic", durable=True, auto_delete=False)


class CeleryConfig:
    task_serializer = "pickle"
    result_serializer = "pickle"
    event_serializer = "json"
    accept_content = ["application/json", "application/x-python-serialize"]
    result_accept_content = ["application/json", "application/x-python-serialize"]
    redis_backend_health_check_interval = 5
    redis_socket_keepalive = True
    redis_socket_timeout = 60 * 10
    redis_retry_on_timeout = True
    task_compression = "gzip"
    broker_url = config["celery"]["broker_url"]
    result_backend = config["celery"]["result_backend"]
    include = ["app.task.job", "app.task.crontab"]
    task_routes = [
        {
            "app.task.job.*": {
                "queue": "meepo_celery_job",
                "routing_key": "meepo_job",
            }
        },
        {
            "app.task.crontab.*": {
                "queue": "meepo_celery_crontab",
                "routing_key": "meepo_cron",
            }
        },
    ]
    beat_schedule = {
        "add-every-minute": {
            "task": "app.task.crontab.example.crontab_example_add",
            "schedule": crontab(minute="*/1"),
            "args": (16, 16),
        }
    }


def init_celery() -> Celery:
    celery_instance: Celery = Celery()
    celery_instance.config_from_object(CeleryConfig)
    celery_instance.autodiscover_tasks([])
    celery_instance.conf.task_queues = (
        Queue("meepo_celery_job", exchange=DEFAULT_EXCHANGE, routing_key="meepo_job"),
        Queue("meepo_celery_crontab", exchange=DEFAULT_EXCHANGE, routing_key="meepo_cron"),
    )

    return celery_instance


@worker_process_init.connect
def config_db(**kwargs: dict) -> None:
    logger.info("celery instance init")
    asyncio.set_event_loop(asyncio.new_event_loop())
    from app.config.base import Container
    from app.config.init import mongo_init, mysql_init

    # 链接初始化
    container = Container()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(mongo_init(container))
    loop.run_until_complete(mysql_init(container))
