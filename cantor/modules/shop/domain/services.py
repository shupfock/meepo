from typing import Optional

from .entities import Shop
from .repositoies import ShopRepository


class ShopDomain:
    def __init__(self, shop_repository: ShopRepository):
        self.shop_repository = shop_repository

    async def create_shop(self, name: str, address: str, logo: str) -> Shop:
        shop = Shop(
            id=0,
            name=name,
            address=address,
            logo=logo,
        )
        return await self.shop_repository.insert(shop)

    async def get_shop_by_id(self, shop_id: int) -> Optional[Shop]:
        return await self.shop_repository.get_by_id(shop_id)
