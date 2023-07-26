from pydantic import BaseModel


class BaseTODOItem(BaseModel):
    name: str
    description: str | None = None


class UpdateTODOItem(BaseModel):
    name: str | None = None
    description: str | None = None


class TODOItem(BaseTODOItem):
    id: int

