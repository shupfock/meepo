from pydantic import BaseModel


class ShopInfo(BaseModel):
    id: int
    name: str
    address: str
    logo: str
    status: int


class CreateShopData(BaseModel):
    shop_id: int
