from typing import List, Optional, Type, TypeVar

from beanie import Document, PydanticObjectId

from cantor.seedwork.domain.entities import MongoEntity
from cantor.utils.logger import get_logger
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


class MongoModelRegister:
    def __init__(self, database_name: str = "cantor"):
        self._model_list: List = []
        self._db_name = database_name
        self.database_name = database_name

    def register(self, model: Type[T]) -> Type[T]:
        if issubclass(model, Document):
            self._model_list.append(model)
            logger.debug(f"model {model.__name__} of database:{self.database_name} registered")
        return model

    def model_list(self) -> List[T]:
        return self._model_list


main_database_name = config.get("db", {}).get("mongo", {}).get("main", {}).get("database", "cantor")
mongo_model_register = MongoModelRegister(database_name=main_database_name)
