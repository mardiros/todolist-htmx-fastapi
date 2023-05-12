import uuid

from pydantic import BaseModel, Field


def generate_id() -> str:
    return str(uuid.uuid1())


class TodoListItem(BaseModel):
    id: str = Field(default_factory=generate_id)
    label: str = Field(min_length=2)
