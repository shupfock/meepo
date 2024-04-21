from typing import Optional

from pydantic import BaseModel, Field

from cantor.modules.shop.application.response import CreateShopData, ShopInfo


class BaseResponse(BaseModel):
    status: int = 200
    status_code: int = 1
    data: Optional[BaseModel] = BaseModel()


class CreateShopRequest(BaseModel):
    name: str = Field(min_length=1, max_length=20, description="店名")
    address: str = Field(default="", min_length=0, max_length=50, description="地址")
    logo: str = Field(default="", min_length=0, max_length=200, description="logo地址")


class CreateShopResponse(BaseResponse):
    data: CreateShopData


class GetShopResponse(BaseResponse):
    data: Optional[ShopInfo]
