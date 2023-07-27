from pydantic import BaseModel


class Message(BaseModel):
    message: str


class BaseTodoItem(BaseModel):
    name: str
    description: str | None = None


class UpdateTodoItem(BaseModel):
    name: str | None = None
    description: str | None = None


class TodoItem(BaseTodoItem):
    id: int

