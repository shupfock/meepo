from typing import List, Optional

from ..domain.entities import Author, AuthorIn
from ..domain.repositories import AuthorRepository
from .models import AuthorModel


class AuthorMysqlRepository(AuthorRepository):
    model = AuthorModel

    async def create(self, author: AuthorIn) -> Author:  # type: ignore
        return await Author.from_tortoise_orm(await self.model.create(**author.dict()))  # type: ignore

    async def get_by_id(self, author_id: int) -> Optional[Author]:  # type: ignore
        author = await self.model.filter(pk=author_id).first()
        return await Author.from_tortoise_orm(author) if author else None

    async def list_by_name(self, name: str) -> List[Author]:  # type: ignore
        authors = self.model.filter(name__contains=name)
        return await Author.from_queryset(authors)
