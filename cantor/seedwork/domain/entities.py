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

    @property
    def oid(self) -> str:
        return str(self.id)


class MysqlEntity(Entity):

    id: int
