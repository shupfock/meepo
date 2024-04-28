from sqlalchemy import Column, DateTime, Integer, SmallInteger, String

from app.seedwork.infrastructure.repository import BaseRDSMainodel


class ShopRDSModel(BaseRDSMainodel):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer)
    created = Column(DateTime)
    updated = Column(DateTime)
    name = Column(String(20))
    address = Column(String(100))
    logo = Column(String(500))
    status = Column(SmallInteger)
