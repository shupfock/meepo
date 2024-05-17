from dependency_injector import providers

from app.config.base import Container
from app.modules.author.infrastructure.author_repository import AuthorMysqlRepository
from app.modules.shop.infrastructure.shop_repository import ShopMysqlRepositoy


class ShopInfrastructureContainer(Container):
    shop_mysql_repo = providers.Factory(ShopMysqlRepositoy, session=Container.mysql.provided.main_session)


class AuthorInfrastructureContainer(Container):
    auth_mysql_repo = providers.Factory(AuthorMysqlRepository)
