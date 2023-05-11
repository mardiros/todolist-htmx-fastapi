from pydantic import BaseModel, Field


class TodoListItem(BaseModel):
    label: str = Field(min_length=2)
