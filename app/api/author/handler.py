from app.api.shared import APIRouter, dependency
from app.config.modules.author_container import AuthorServiceContainer
from app.modules.author.application.services import AuthorService

from .models import CreateAuthorRequest, CreateAuthorResponse, GetAuthorResponse, ListAuthorResponse

author_router = APIRouter(prefix="/api/author", tags=["author"])


@author_router.post("/create", response_model=CreateAuthorResponse, name="创建作者")
async def create_author(
    req: CreateAuthorRequest,
    service: AuthorService = dependency(AuthorServiceContainer.author_service),
) -> CreateAuthorResponse:
    data = await service.create_author(req.name, req.sex)

    return CreateAuthorResponse(data=data)


@author_router.get("/get", response_model=GetAuthorResponse, name="获取一个 author")
async def get_author(
    author_id: int,
    service: AuthorService = dependency(AuthorServiceContainer.author_service),
) -> GetAuthorResponse:
    data = await service.get_author_by_id(author_id)

    return GetAuthorResponse(data=data)


@author_router.get("/list", response_model=ListAuthorResponse, name="获取 author 列表")
async def list_author(
    name: str,
    service: AuthorService = dependency(AuthorServiceContainer.author_service),
) -> ListAuthorResponse:
    data = await service.list_author_by_name(name)

    return ListAuthorResponse(data=data)
