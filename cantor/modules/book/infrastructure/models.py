import pymongo

from cantor.modules.book.domain.entities import Book
from cantor.seedwork.infrastructure.repository import BaseMongoMainModel


class BookMongoModel(Book, BaseMongoMainModel):
    class Settings:
        name = "book"
        indexes = [[("name", pymongo.ASCENDING)]]
