from abc import ABC, abstractmethod
from typing import List, Optional

from .entities import Book


class BookRepository(ABC):
    @abstractmethod
    async def get_book_by_name(self, name: str) -> Optional[Book]:
        raise NotImplementedError

    @abstractmethod
    async def list_books_by_count(self, c: int) -> List[Book]:
        raise NotImplementedError

    @abstractmethod
    async def add_book(self, book: Book) -> Book:
        raise NotImplementedError

    @abstractmethod
    async def delete_book_by_id(self, book_id: str) -> None:
        raise NotImplementedError
