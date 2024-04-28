from dependency_injector import providers

from app.config.base import Container
from app.modules.book.infrastructure.book_repository import BookMongoRepository


class BookInfrastructureContainer(Container):
    book_mongo_repo = providers.Factory(BookMongoRepository)
