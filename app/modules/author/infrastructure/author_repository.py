from typing import List, Optional, cast

from ..domain.entities import Author, IAuthor
from ..domain.repositories import AuthorRepository
from .models import AuthorModel


class AuthorMysqlRepository(AuthorRepository):
    model = AuthorModel

    async def create(self, author: IAuthor) -> Author:
        return cast(Author, await Author.from_tortoise_orm(await self.model.create(**author.dict())))

    async def get_by_id(self, author_id: int) -> Optional[Author]:
        author = await self.model.filter(pk=author_id).first()
        return cast(Author, await Author.from_tortoise_orm(author)) if author else None

    async def list_by_name(self, name: str) -> List[Author]:
        authors = self.model.filter(name__contains=name)
        return cast(List[Author], await Author.from_queryset(authors))
