import pymongo

from app.modules.book.domain.entities import Book
from app.seedwork.infrastructure.repository import BaseMongoMainModel


class BookMongoModel(Book, BaseMongoMainModel):
    class Settings:
        name = "book"
        indexes = [[("name", pymongo.ASCENDING)]]
