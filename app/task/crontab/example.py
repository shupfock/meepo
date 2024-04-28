from app.task import celery
from app.utils.logger import get_logger

logger = get_logger()


@celery.task
def crontab_example_add(first: int, second: int) -> None:
    response = first + second
    logger.info(f"crontab_example result:{response}")
