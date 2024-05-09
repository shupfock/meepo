from typing import Optional

from tortoise.transactions import atomic

from ..domain.entities import IAuthor
from ..domain.repositories import AuthorRepository
from ..domain.services import AuthorDomain
from .response import AuthorInfo, AuthorListData


class AuthorService:
    def __init__(self, author_repository: AuthorRepository):
        self.author_domain = AuthorDomain(author_repository=author_repository)

    @atomic()
    async def create_author(self, name: str, sex: int) -> AuthorInfo:
        iauthor = IAuthor(name=name, sex=sex)
        author = await self.author_domain.create_author(iauthor)
        return AuthorInfo.parse_obj(author.dict())

    async def get_author_by_id(self, author_id: int) -> Optional[AuthorInfo]:
        author = await self.author_domain.get_author_by_id(author_id)
        return AuthorInfo.parse_obj(author.dict()) if author else None

    async def list_author_by_name(self, name: str) -> AuthorListData:
        authors = await self.author_domain.list_author_by_name(name)
        return AuthorListData(list=[AuthorInfo.parse_obj(a.dict()) for a in authors])
