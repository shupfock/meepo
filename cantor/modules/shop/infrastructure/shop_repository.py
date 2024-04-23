from typing import Optional

from redis.asyncio import Redis
from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession

from ..domain.entities import Shop
from ..domain.repositoies import ShopCacheRepository, ShopRepository
from .models import ShopRDSModel


class ShopMysqlRepositoy(ShopRepository):
    model = ShopRDSModel

    async def insert(self, session: AsyncSession, shop: Shop) -> Shop:
        data = shop.dict()
        data.pop("id", None)
        shop_orm = self.model(**data)
        session.add(shop_orm)
        await session.flush()

        return Shop.parse_obj(shop_orm.__dict__)

    async def get_by_id(self, session: AsyncSession, shop_id: int) -> Optional[Shop]:
        result: Result = await session.execute(Select(self.model).filter(self.model.id == shop_id).limit(1))
        shop_orm = result.scalar_one_or_none()
        if not shop_orm:
            return None

        return Shop.parse_obj(shop_orm.__dict__)


class ShopCacheRedisRepository(ShopCacheRepository):

    SHOP_NUM_KEY = "cantor:shop_num"

    def __init__(self, conn: Redis):
        self.conn = conn

    async def gen_shop_num(self) -> int:
        return await self.conn.incr(self.SHOP_NUM_KEY)
