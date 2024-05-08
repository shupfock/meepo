from typing import Optional, Union

from pydantic import BaseModel, Field

from app.modules.author.application.response import AuthorInfo, AuthorListData


class BaseResponse(BaseModel):
    status: int = 200
    status_code: int = 1
    data: Optional[Union[dict, BaseModel]] = {}


class CreateAuthorRequest(BaseModel):
    name: str = Field(max_length=20, description="姓名")
    sex: int = Field(ge=1, le=2, description="性别")


class CreateAuthorResponse(BaseResponse):
    data: AuthorInfo


class GetAuthorResponse(BaseResponse):
    data: Optional[AuthorInfo]


class ListAuthorResponse(BaseResponse):
    data: AuthorListData
