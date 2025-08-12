from datetime import datetime

from pydantic import BaseModel


class SessionDTO(BaseModel):

    id: int
    user_id: str | None
    created_at: datetime
