from dependency_injector import providers

from app.config.base import Container
from app.config.infrastructure.mysql_factory import AuthorInfrastructureContainer
from app.config.init import container_init
from app.modules.author.application.services import AuthorService


@container_init.aotu_wired
class AuthorServiceContainer(Container):
    author_service = providers.Factory(
        AuthorService,
        author_repository=AuthorInfrastructureContainer.auth_mysql_repo,
    )
