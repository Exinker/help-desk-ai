import re

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase

from config import DB_CONFIG


class BaseModel(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    metadata = MetaData(
        naming_convention=DB_CONFIG.naming_convention,
        schema=DB_CONFIG.schema,
    )

    @declared_attr
    def __tablename__(cls) -> str:

        name = cls.__name__
        name = re.sub(r'Model$', '', name)
        name = re.sub('([a-z])([A-Z])', r'\1_\2', name)

        return name.lower()
