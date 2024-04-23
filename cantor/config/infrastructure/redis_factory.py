from dependency_injector import providers

from cantor.config.base import Container
from cantor.modules.shop.infrastructure.shop_repository import ShopCacheRedisRepository


class ShopRedisInfrastructureContainer(Container):

    shop_redis_repo = providers.Singleton(ShopCacheRedisRepository, conn=Container.redis.provided.main)
