from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .entities import Shop
from .repositoies import ShopCacheRepository, ShopRepository


class ShopDomain:
    def __init__(self, shop_repository: ShopRepository, shop_cache_repository: ShopCacheRepository):
        self.shop_repository = shop_repository
        self.shop_cache_repository = shop_cache_repository

    async def create_shop(self, session: AsyncSession, name: str, address: str, logo: str) -> Shop:
        num = await self.shop_cache_repository.gen_shop_num()
        shop = Shop(
            id=0,
            num=num,
            name=name,
            address=address,
            logo=logo,
        )
        return await self.shop_repository.insert(session, shop)

    async def get_shop_by_id(self, shop_id: int) -> Optional[Shop]:
        return await self.shop_repository.get_by_id(shop_id)
