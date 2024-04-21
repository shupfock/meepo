import pymongo
from beanie import Document

from cantor.modules.book.domain.entities import Book
from cantor.seedwork.infrastructure.repository import mongo_model_register


@mongo_model_register.register
class BookMongoModel(Book, Document):
    class Settings:
        name = "book"
        indexes = [[("name", pymongo.ASCENDING)]]
