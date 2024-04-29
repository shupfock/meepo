from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.repositoies import ShopCacheRepository, ShopRepository
from ..domain.services import ShopDomain
from .response import CreateShopData, ShopInfo


class ShopService:
    def __init__(
        self,
        shop_repository: ShopRepository,
        shop_cache_repository: ShopCacheRepository,
        session: AsyncSession,
    ):
        self.session = session
        self.shop_domain = ShopDomain(shop_repository=shop_repository, shop_cache_repository=shop_cache_repository)

    async def create_shop(self, name: str, address: str, logo: str) -> CreateShopData:
        async with self.session.begin():
            shop = await self.shop_domain.create_shop(name, address, logo)

            return CreateShopData(shop_id=shop.id)

    async def get_shop_by_id(self, shop_id: int) -> Optional[ShopInfo]:
        shop = await self.shop_domain.get_shop_by_id(shop_id)
        if not shop:
            return None

        return ShopInfo.parse_obj(shop)
