from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel, Field
from pydantic_factories import ModelFactory


class Entity(BaseModel):
    @classmethod
    def generate_fake_data(cls):
        class FakeFactory(ModelFactory):
            __model__ = cls

        return FakeFactory.build()


class MongoEntity(Entity):

    id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    created: datetime = Field(default_factory=datetime.now, description="创建时间")
    updated: datetime = Field(default_factory=datetime.now, description="更新时间")

    @property
    def oid(self) -> str:
        return str(self.id)


class MysqlEntity(Entity):

    id: int
