from dependency_injector import providers

from cantor.modules.book.infrastructure.book_repository import BookMongoRepository

from ..base import Container


class BookInfrastructureContainer(Container):
    book_mongo_repo = providers.Factory(BookMongoRepository)
