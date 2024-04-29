from dependency_injector import providers

from app.config.base import Container
from app.config.infrastructure.mysql_factory import ShopInfrastructureContainer
from app.config.infrastructure.redis_factory import ShopRedisInfrastructureContainer
from app.config.init import container_init
from app.modules.shop.application.services import ShopService


@container_init.aotu_wired
class ShopServiceContainer(Container):

    shop_service = providers.Factory(
        ShopService,
        session=Container.mysql.provided.main_session,
        shop_repository=ShopInfrastructureContainer.shop_mysql_repo,
        shop_cache_repository=ShopRedisInfrastructureContainer.shop_redis_repo,
    )
