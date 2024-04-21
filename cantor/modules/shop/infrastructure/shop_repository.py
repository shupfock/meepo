from typing import Optional

from sqlalchemy import Result, Select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from ..domain.entities import Shop
from ..domain.repositoies import ShopRepository
from .models import ShopRDSModel


class ShopMysqlRepositoy(ShopRepository):
    model = ShopRDSModel

    def __init__(self, session: async_sessionmaker[AsyncSession]):
        self.session = session

    async def insert(self, shop: Shop) -> Shop:
        data = shop.dict()
        data.pop("id", None)
        shop_orm = self.model(**data)
        async with self.session() as session:
            session.add(shop_orm)
            await session.flush()
            await session.commit()

        return Shop.parse_obj(shop_orm.__dict__)

    async def get_by_id(self, shop_id: int) -> Optional[Shop]:
        async with self.session() as session:
            result: Result = await session.execute(Select(self.model).filter(self.model.id == shop_id).limit(1))
            shop_orm = result.scalar_one_or_none()
            if not shop_orm:
                return None

            return Shop.parse_obj(shop_orm.__dict__)
