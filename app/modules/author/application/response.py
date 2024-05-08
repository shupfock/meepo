from datetime import datetime
from typing import List

from pydantic import BaseModel


class AuthorInfo(BaseModel):
    id: int
    name: str
    sex: int
    status: bool
    created: datetime


class AuthorListData(BaseModel):
    list: List[AuthorInfo]
