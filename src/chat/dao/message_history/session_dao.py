from pydantic import BaseModel

from chat.dto import SessionDTO
from chat.dao.database.models import SessionModel


class CreateSessionTask(BaseModel):

    task_id: int
    user_id: str | None


class GetSessionTask(BaseModel):

    task_id: int
    session_id: int


class SessionDAO:

    def create(self, task: CreateSessionTask) -> SessionDTO:
        pass

    def get(self, task: GetSessionTask) -> SessionDTO:
        pass
