from typing import List, Optional

from beanie import PydanticObjectId
from beanie.operators import GT, Set

from cantor.seedwork.infrastructure.repository import GenericMongoRepository

from ..domain.entities import Book, BookStatus
from ..domain.repositories import BookRepository
from .models import BookMongoModel


class BookMongoRepository(BookRepository, GenericMongoRepository):
    model = BookMongoModel

    async def get_book_by_name(self, name: str) -> Optional[Book]:
        target = await self.model.find_one({self.model.name: name})
        return Book.parse_obj(target) if target else None

    async def list_books_by_count(self, c: int) -> List[Book]:
        target_list = await self.model.find(GT(self.model.count, c)).to_list()

        return [Book.parse_obj(t) for t in target_list]

    async def add_book(self, book: Book) -> Book:
        target = self.model.parse_obj(book)
        await target.create()
        return Book.parse_obj(target)

    async def delete_book_by_id(self, book_id: str) -> None:
        if not PydanticObjectId.is_valid(book_id):
            return
        await self.model.find_one(self.model.id == PydanticObjectId(book_id)).update_one(
            Set({self.model.status: BookStatus.DELETE})
        )
