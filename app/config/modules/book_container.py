from dependency_injector import providers

from app.config.base import Container
from app.config.infrastructure.mongo_factory import BookInfrastructureContainer
from app.config.init import container_init
from app.modules.book.application.services import BookService


@container_init.aotu_wired
class BookServiceContainer(Container):
    book_service = providers.Factory(
        BookService,
        book_repository=BookInfrastructureContainer.book_mongo_repo,
    )
