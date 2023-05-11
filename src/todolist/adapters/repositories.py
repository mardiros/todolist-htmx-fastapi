import abc
from typing import Sequence

from todolist.domain.model import TodoListItem


class AbstractTodoListRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: TodoListItem) -> None:
        ...

    @abc.abstractmethod
    def list(self) -> Sequence[TodoListItem]:
        ...


class InMemoryTodoListRepository(AbstractTodoListRepository):
    items = []

    def add(self, item: TodoListItem) -> None:
        self.items.append(item)

    def list(self) -> Sequence[TodoListItem]:
        return self.items