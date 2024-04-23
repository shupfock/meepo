from enum import IntEnum

from pydantic import Field

from cantor.seedwork.domain.entities import MysqlEntity


class ShopStatus(IntEnum):
    NORMAL = 1
    DELETE = 0


class Shop(MysqlEntity):

    id: int = Field(description="店铺 ID")
    num: int = Field(description="店铺号")
    name: str = Field(description="店铺名")
    address: str = Field(description="店铺地址")
    logo: str = Field(description="店铺 logo")
    status: ShopStatus = Field(default=ShopStatus.NORMAL, description="店铺状态")
