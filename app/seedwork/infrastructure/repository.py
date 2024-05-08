from typing import Optional, Type, TypeVar

from beanie import Document, PydanticObjectId
from sqlalchemy.ext.declarative import declarative_base
from tortoise import Model, fields

from app.seedwork.domain.entities import MongoEntity
from app.utils.logger import get_logger
from settings import config

logger = get_logger()

T = TypeVar("T", bound=Document)
E = TypeVar("E", bound=MongoEntity)


class GenericMongoRepository:
    @staticmethod
    async def get_element_by_id(model: Type[T], element_id: str) -> Optional[T]:
        if not PydanticObjectId.is_valid(element_id):
            return None
        return await model.find_one(document_id=PydanticObjectId(element_id))


def declarative_mongo_base(name):
    class CustomBaseMongoModel(Document):
        pass

    CustomBaseMongoModel.__name__ = name

    return CustomBaseMongoModel


def declarative_mysql_base(name):
    class CustomBaseMysqlModel(Model):
        id = fields.BigIntField(pk=True, index=True)

        class Meta:
            abstract = True

    CustomBaseMysqlModel.__name__ = name

    return CustomBaseMysqlModel


mongo_main_database_name = config.get("db", {}).get("mongo", {}).get("main", {}).get("database", "cantor")
BaseMongoMainModel = declarative_mongo_base(mongo_main_database_name)

mysql_main_data_name = config.get("db", {}).get("mysql", {}).get("main", {}).get("database", "cantor")
BaseRDSMainModel = declarative_base(name=mysql_main_data_name)

mysql_tortoise_data_name = config.get("db", {}).get("mysql", {}).get("tortoise", {}).get("database", "tortoise")
BaseRDSTortoiseModel = declarative_mysql_base(name=mysql_tortoise_data_name)
