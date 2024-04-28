from typing import Optional

from ..domain.entities import Book
from ..domain.repositories import BookRepository
from ..domain.services import BookDomain
from .response import AddBookData, BookInfo, ListBookData


class BookService:
    def __init__(self, book_repository: BookRepository):
        self.book_domain = BookDomain(book_repository)

    async def add_book(self, name: str, count: int) -> AddBookData:
        book = await self.book_domain.add_book(name, count)

        return AddBookData(book_id=book.oid)

    @staticmethod
    def format_book(book: Book) -> BookInfo:
        return BookInfo(
            id=book.oid,
            name=book.name,
            count=book.count,
            status=book.status,
        )

    async def get_book_by_name(self, name: str) -> Optional[BookInfo]:
        book = await self.book_domain.get_book_by_name(name)
        if not book:
            return None
        return self.format_book(book)

    async def list_book_by_count(self, count: int) -> ListBookData:
        books = await self.book_domain.list_books_by_count(count)
        return ListBookData(data_list=[self.format_book(b) for b in books])

    async def delete_book_by_id(self, book_id: str) -> None:
        await self.book_domain.delete_book(book_id)
