from dependency_injector import providers

from cantor.config.base import Container
from cantor.config.infrastructure.mysql_factory import ShopInfrastructureContainer
from cantor.config.infrastructure.redis_factory import ShopRedisInfrastructureContainer
from cantor.config.init import container_init
from cantor.modules.shop.application.services import ShopService


@container_init.aotu_wired
class ShopServiceContainer(Container):
    shop_service = providers.Factory(
        ShopService,
        session_maker=Container.mysql_session_maker,
        shop_repository=ShopInfrastructureContainer.shop_mysql_repo,
        shop_cache_repository=ShopRedisInfrastructureContainer.shop_redis_repo,
    )
