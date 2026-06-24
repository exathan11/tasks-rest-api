from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str


class TaskUpdate(BaseModel):
    name: str
    status: str


class TaskResponse(BaseModel):
    id: int
    name: str
    status: str
