from enum import IntEnum

from tortoise import fields

from app.seedwork.infrastructure.repository import BaseRDSTortoiseModel


class AuthorSex(IntEnum):
    MAN = 1
    FEMALE = 2


class AuthorModel(BaseRDSTortoiseModel):
    created = fields.DatetimeField(auto_now_add=True, description="创建时间")
    name = fields.CharField(max_length=20, description="姓名")
    sex = fields.IntEnumField(AuthorSex, description="性别")
    status = fields.BooleanField(default=True, description="是否删除")

    class Meta:
        table = "author"
