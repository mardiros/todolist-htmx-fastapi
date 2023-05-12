import abc
from typing import Sequence

from todolist.domain.model import TodoListItem


class AbstractTodoListRepository(abc.ABC):
    @abc.abstractmethod
    async def add(self, item: TodoListItem) -> None:
        ...

    @abc.abstractmethod
    async def remove(self, item: TodoListItem) -> None:
        ...

    @abc.abstractmethod
    async def list(self) -> Sequence[TodoListItem]:
        ...
