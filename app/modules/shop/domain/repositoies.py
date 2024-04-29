from abc import ABC, abstractmethod
from typing import Optional

from .entities import Shop


class ShopRepository(ABC):
    @abstractmethod
    async def insert(self, shop: Shop) -> Shop:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, shop_id: int) -> Optional[Shop]:
        raise NotImplementedError


class ShopCacheRepository(ABC):
    @abstractmethod
    async def gen_shop_num(self) -> int:
        raise NotImplementedError
