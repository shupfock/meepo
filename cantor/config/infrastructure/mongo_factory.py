from dependency_injector import providers

from cantor.config.base import Container
from cantor.modules.book.infrastructure.book_repository import BookMongoRepository


class BookInfrastructureContainer(Container):
    book_mongo_repo = providers.Factory(BookMongoRepository)
