from fastapi import Query

from cantor.config.modules.book_container import BookServiceContainer
from cantor.modules.book.application.services import BookService

from ...shared import APIRouter, dependency
from .models import AddBookRequest, AddBookResponse, GetBookResponse, ListBookResponse

book_router = APIRouter(prefix="/api/book", tags=["book"])


@book_router.post("/add", response_model=AddBookResponse, name="添加一本书")
async def add_book(
    req: AddBookRequest, service: BookService = dependency(BookServiceContainer.book_service)
) -> AddBookResponse:
    data = await service.add_book(req.name, req.count)

    return AddBookResponse(data=data)


@book_router.get("/get", response_model=GetBookResponse, name="查询一本书")
async def get_book_by_name(
    name: str = Query(max_length=20, description="书名"),
    service: BookService = dependency(BookServiceContainer.book_service),
) -> GetBookResponse:
    data = await service.get_book_by_name(name)

    return GetBookResponse(data=data)


@book_router.get("/list", response_model=ListBookResponse, name="查询数量大于值的书")
async def list_book_by_count(
    count: int = Query(description="书的数量"),
    service: BookService = dependency(BookServiceContainer.book_service),
) -> ListBookResponse:
    data = await service.list_book_by_count(count)

    return ListBookResponse(data=data)
