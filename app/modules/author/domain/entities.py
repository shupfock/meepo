from datetime import datetime

from tortoise.contrib.pydantic import PydanticModel


class Author(PydanticModel):
    id: int
    created: datetime
    name: str
    sex: int
    status: int


class IAuthor(PydanticModel):
    name: str
    sex: int
