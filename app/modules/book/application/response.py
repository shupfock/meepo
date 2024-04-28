from typing import List

from pydantic import BaseModel, Field


class BookInfo(BaseModel):
    id: str = Field(description="")
    name: str = Field(description="")
    count: int = Field(description="")
    status: int = Field(description="")


class AddBookData(BaseModel):
    book_id: str = Field(description="书本 ID")


class ListBookData(BaseModel):
    data_list: List[BookInfo]
