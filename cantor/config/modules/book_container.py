from dependency_injector import providers

from cantor.config.base import Container
from cantor.config.infrastructure.mongo_factory import BookInfrastructureContainer
from cantor.config.init import container_init
from cantor.modules.book.application.services import BookService


@container_init.aotu_wired
class BookServiceContainer(Container):
    book_service = providers.Factory(
        BookService,
        book_repository=BookInfrastructureContainer.book_mongo_repo,
    )
