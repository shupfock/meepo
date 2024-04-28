from typing import Optional

from pydantic import BaseModel, Field

from app.modules.book.application.response import AddBookData, BookInfo, ListBookData


class BaseResponse(BaseModel):
    status: int = 200
    status_code: int = 1
    data: Optional[BaseModel] = BaseModel()


class AddBookRequest(BaseModel):
    name: str = Field(min_length=1, max_length=20, description="书名")
    count: int = Field(gt=0, lt=10000, description="书数量")


class AddBookResponse(BaseResponse):
    data: AddBookData


class GetBookResponse(BaseResponse):
    data: Optional[BookInfo]


class ListBookResponse(BaseResponse):
    data: ListBookData
