from dependency_injector import providers

from cantor.modules.book.application.services import BookService

from ..base import Container
from ..infrastructure.mongo_factory import BookInfrastructureContainer
from ..init import container_init


@container_init.aotu_wired
class BookServiceContainer(Container):
    book_service = providers.Factory(
        BookService,
        book_repository=BookInfrastructureContainer.book_mongo_repo,
    )
