import importlib
import inspect
import os
from typing import Dict, Optional, Type, TypeVar

from app.config.base import Container
from app.seedwork.infrastructure.repository import BaseMongoMainModel, BaseRDSMainModel, BaseRDSTortoiseModel
from app.utils.logger import get_logger

T = TypeVar("T", bound=Container)

logger = get_logger()


def find_mongo_module_to_init() -> None:
    importlib.import_module("app.config.infrastructure.mongo_factory")


async def mongo_init(container: Container) -> None:
    find_mongo_module_to_init()
    mongo = container.mongo()
    main_database = mongo.main.get_database(BaseMongoMainModel.__name__)
    await container.init_odm_model(database=main_database, document_models=BaseMongoMainModel.__subclasses__())
    logger.info("mogno orm models init")


async def redis_init(container: Container) -> None:
    redis = container.redis()
    await redis.main.ping()
    logger.info("redis ping success")


async def mysql_init(container: Container) -> None:
    mysql = container.mysql()
    async with mysql.main.begin() as conn:
        await conn.run_sync(BaseRDSMainModel.metadata.create_all)
        await conn.commit()
    logger.info("mysql orm models init")


async def mysql_tortoise_init(container: Container) -> None:
    mysql = container.mysql()
    models = set()
    for sub_model in BaseRDSTortoiseModel.__subclasses__():
        path = os.path.relpath(inspect.getfile(sub_model))
        path = path.rstrip(".py").replace("/", ".")
        models.add(path)

    await container.init_rdm_model(**mysql.tortoise, modules={"models": list(models)})
    await container.generate_schemas()


class ContainerInitializer:
    map_container_name_instance: Dict[str, Container] = {}

    def aotu_wired(self, container: Type[T]) -> Type[T]:
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
