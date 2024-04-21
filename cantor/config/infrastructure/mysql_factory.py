from dependency_injector import providers

from cantor.config.base import Container
from cantor.modules.shop.infrastructure.shop_repository import ShopMysqlRepositoy


class ShopInfrastructureContainer(Container):

    shop_mysql_repo = providers.Factory(
        ShopMysqlRepositoy,
        session=Container.mysql_session,
    )
