import importlib
from typing import Dict, Optional, Type, TypeVar

from cantor.config.base import Container
from cantor.seedwork.infrastructure.repository import mongo_model_register
from cantor.utils.logger import get_logger

T = TypeVar("T", bound=Container)

logger = get_logger()


def find_mongo_module_to_init() -> None:
    importlib.import_module("cantor.config.infrastructure.mongo_factory")


async def mongo_init(container: Container) -> None:
    find_mongo_module_to_init()
    mongo = container.mongo()
    main_database = mongo.main.get_database(mongo_model_register.database_name)
    await container.init_odm_model(database=main_database, document_models=mongo_model_register.model_list())
    logger.info("mogno orm models init")


async def redis_init(container: Container) -> None:
    redis = container.redis()
    await redis.main.ping()
    logger.info("redis ping success")


class ContainerInitializer:
    map_container_name_instance: Dict[str, Container] = {}

    def aotu_wire(self, container: Type[T]) -> Type[T]:
        if issubclass(container, Container):
            container_name = container.__name__
            target_container = self.map_container_name_instance.get(container_name)
            if not target_container:
                target_container = container()
                self.map_container_name_instance[container_name] = target_container

        return container

    @classmethod
    def get_container_instance_by_name(cls, container_name: str) -> Optional[Container]:
        return cls.map_container_name_instance.get(container_name)


container_init = ContainerInitializer()
