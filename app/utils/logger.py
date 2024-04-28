import logging
import sys
from types import FrameType
from typing import cast

from loguru import logger

from settings import config


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:  # pragma: no cover
        # Get corresponding Loguru level if it exists
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = str(record.levelno)

        # Find caller from where originated the logged message
        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:  # noqa: WPS609
            frame = cast(FrameType, frame.f_back)
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level,
            record.getMessage(),
        )


def init_logger():
    project_config = config.get("project", {})
    if project_config.get("log_level") == "debug":
        log_level = "DEBUG"
    else:
        log_level = "INFO"

    loguru_handlers = [
        {
            "sink": sys.stdout,
            "level": log_level,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | {thread.name} | <level>{level}</level> | "
            "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        }
    ]

    loggers = (logging.getLogger(name) for name in logging.root.manager.loggerDict if name.startswith("uvicorn."))
    for uvicorn_logger in loggers:
        uvicorn_logger.handlers.clear()

    # change handler for default uvicorn logger
    intercept_handler = InterceptHandler()
    logging.getLogger("uvicorn").handlers = [intercept_handler]

    logger.configure(handlers=loguru_handlers)
    logger.debug("logger init")


init_logger()


def get_logger():
    return logger
