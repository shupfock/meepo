from enum import IntEnum

from pydantic import Field

from app.seedwork.domain.entities import MongoEntity


class BookStatus(IntEnum):
    NORMAL = 1
    DELETE = 0


class Book(MongoEntity):
    name: str = Field(description="书名")
    count: int = Field(default=0, description="数量")
    status: BookStatus = Field(default=BookStatus.NORMAL, description="状态")
