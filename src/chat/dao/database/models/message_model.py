from enum import Enum
from datetime import datetime
from typing import Literal

from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base_model import BaseModel


class MessageRole(Enum):

    SYSTEM = 'system'
    USER = 'user'
    ASSISTANT = 'assistant'


class MessageModel(BaseModel):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey('session.id'))
    role: Mapped[MessageRole]
    text: Mapped[str]
    created_at: Mapped[datetime]
