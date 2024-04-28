from fastapi import Query

from app.api.shared import APIRouter, dependency
from app.config.modules.shop_container import ShopServiceContainer
from app.modules.shop.application.services import ShopService

from .models import CreateShopRequest, CreateShopResponse, GetShopResponse

shop_router = APIRouter(prefix="/api/shop", tags=["shop"])


@shop_router.post("/create", response_model=CreateShopResponse, name="创建店铺")
async def create_shop(
    req: CreateShopRequest,
    service: ShopService = dependency(ShopServiceContainer.shop_service),
) -> CreateShopResponse:
    data = await service.create_shop(req.name, req.address, req.logo)

    return CreateShopResponse(data=data)


@shop_router.get("/get", response_model=GetShopResponse, name="获取店铺")
async def get_shop(
    shop_id: int = Query(gt=0, description="店铺 ID"),
    service: ShopService = dependency(ShopServiceContainer.shop_service),
) -> GetShopResponse:
    data = await service.get_shop_by_id(shop_id)

    return GetShopResponse(data=data)
