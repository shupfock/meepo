from dependency_injector import providers

from app.config.base import Container
from app.modules.shop.infrastructure.shop_repository import ShopMysqlRepositoy


class ShopInfrastructureContainer(Container):

    shop_mysql_repo = providers.Factory(
        ShopMysqlRepositoy,
    )
