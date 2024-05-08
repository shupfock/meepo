from typing import List, Optional

from .entities import Author, AuthorIn
from .repositories import AuthorRepository


class AuthorDomain:
    def __init__(self, author_repository: AuthorRepository):
        self.author_repository = author_repository

    async def create_author(self, author: AuthorIn) -> Author:  # type: ignore[valid-type]
        return await self.author_repository.create(author)

    async def get_author_by_id(self, author_id: int) -> Optional[Author]:  # type: ignore[valid-type]
        return await self.author_repository.get_by_id(author_id)

    async def list_author_by_name(self, name: str) -> List[Author]:  # type: ignore[valid-type]
        return await self.author_repository.list_by_name(name)
