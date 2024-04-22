from dependency_injector import providers

from cantor.config.base import Container
from cantor.config.infrastructure.mysql_factory import ShopInfrastructureContainer
from cantor.config.init import container_init
from cantor.modules.shop.application.services import ShopService


@container_init.aotu_wired
class ShopServiceContainer(Container):
    shop_service = providers.Factory(
        ShopService,
        session=Container.mysql_session,
        shop_repository=ShopInfrastructureContainer.shop_mysql_repo,
    )
