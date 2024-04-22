from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .entities import Shop
from .repositoies import ShopRepository


class ShopDomain:
    def __init__(self, session: AsyncSession, shop_repository: ShopRepository):
        self.session = session
        self.shop_repository = shop_repository

    async def create_shop(self, name: str, address: str, logo: str) -> Shop:
        shop = Shop(
            id=0,
            name=name,
            address=address,
            logo=logo,
        )
        return await self.shop_repository.insert(self.session, shop)

    async def get_shop_by_id(self, shop_id: int) -> Optional[Shop]:
        return await self.shop_repository.get_by_id(self.session, shop_id)
