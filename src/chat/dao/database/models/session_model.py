from sqlalchemy import Integer
from sqlalchemy.orm import Mapped, mapped_column

from database.models.base_model import BaseModel


class SessionModel(BaseModel):

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[str | None]
