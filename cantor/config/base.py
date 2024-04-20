from typing import Optional

from beanie import init_beanie
from dependency_injector import containers, providers
from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis

from settings import config as app_config


class CantorMongo:
    def __init__(self):
        self._main: Optional[AgnosticClient] = None

    def init(self, mongo_config: dict) -> None:
        self._main = AsyncIOMotorClient(**mongo_config.get("main", {}))

    @property
    def main(self):
        return self._main


class CantorRedis:
    def __init__(self):
        self._main: Optional[Redis] = None

    def init(self, redis_config: dict) -> None:
        self._main = Redis(**redis_config.get("main", {}))

    @property
    def main(self):
        return self._main


def create_mongo_connect_once(mongo_config: dict) -> CantorMongo:
    mongo = CantorMongo()
    mongo.init(mongo_config)

    return mongo


def create_redis_connect_once(redis_config: dict) -> CantorRedis:
    redis = CantorRedis()
    redis.init(redis_config)

    return redis


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()
    config.from_dict(app_config)

    mongo = providers.Singleton(create_mongo_connect_once, config.get("db").get("mongo", {}))
    redis = providers.Singleton(create_redis_connect_once, config.get("db").get("redis", {}))

    init_odm_model = providers.Callable(init_beanie)
