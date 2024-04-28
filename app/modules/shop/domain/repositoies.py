from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from .entities import Shop


class ShopRepository(ABC):
    @abstractmethod
    async def insert(self, session: AsyncSession, shop: Shop) -> Shop:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, session: AsyncSession, shop_id: int) -> Optional[Shop]:
        raise NotImplementedError


class ShopCacheRepository(ABC):
    @abstractmethod
    async def gen_shop_num(self) -> int:
        raise NotImplementedError
