from asyncio import current_task
from typing import Optional

from beanie import init_beanie
from dependency_injector import containers, providers
from motor.core import AgnosticClient
from motor.motor_asyncio import AsyncIOMotorClient
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

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


class CantorMysql:
    def __init__(self):
        self._main: Optional[AsyncEngine] = None
        self._main_session: Optional[AsyncSession] = None

    def init(self, mysql_config: dict) -> None:
        self._main = create_async_engine(**mysql_config.get("main", {}))

    async def session_factory(self, engine_name: str = "main") -> None:
        async_session = async_scoped_session(
            async_sessionmaker(
                class_=AsyncSession,
                bind=getattr(self, engine_name),
                expire_on_commit=False,
            ),
            scopefunc=current_task,
        )
        async with async_session() as session:
            setattr(self, f"_{engine_name}_session", session)

    @property
    def main(self):
        return self._main

    @property
    async def main_session(self) -> AsyncSession:
        if not self._main_session:
            await self.session_factory()
        assert self._main_session is not None
        return self._main_session


def create_mongo_connect_once(mongo_config: dict) -> CantorMongo:
    mongo = CantorMongo()
    mongo.init(mongo_config)

    return mongo


def create_redis_connect_once(redis_config: dict) -> CantorRedis:
    redis = CantorRedis()
    redis.init(redis_config)

    return redis


def create_mysql_connect_once(mysql_config: dict) -> CantorMysql:
    mysql = CantorMysql()
    mysql.init(mysql_config)

    return mysql


class Container(containers.DeclarativeContainer):
    __self__ = providers.Self()
    config = providers.Configuration()
    config.from_dict(app_config)

    mongo = providers.Singleton(create_mongo_connect_once, config.get("db").get("mongo", {}))
    redis = providers.Singleton(create_redis_connect_once, config.get("db").get("redis", {}))
    mysql = providers.Singleton(create_mysql_connect_once, config.get("db").get("mysql", {}))

    init_odm_model = providers.Callable(init_beanie)
