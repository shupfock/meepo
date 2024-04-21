from typing import List, Optional

from .entities import Book
from .exceptions import BookCountException
from .repositories import BookRepository


class BookDomain:
    def __init__(self, book_repository: BookRepository):
        self.book_repository = book_repository

    async def add_book(self, name: str, count: int) -> Book:
        if count < 0:
            raise BookCountException()

        book = Book(
            name=name,
            count=count,
        )
        book = await self.book_repository.add_book(book)

        return book

    async def get_book_by_name(self, name: str) -> Optional[Book]:
        return await self.book_repository.get_book_by_name(name)

    async def list_books_by_count(self, count: int) -> List[Book]:
        return await self.book_repository.list_books_by_count(count)

    async def delete_book(self, book_id: str) -> None:
        await self.book_repository.delete_book_by_id(book_id)
