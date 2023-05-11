from typing import TYPE_CHECKING, Sequence

from todolist.domain.model import TodoListItem
from todolist.domain.repositories import AbstractTodoListRepository
from todolist.service.unit_of_work import AbstractUnitOfWork

if TYPE_CHECKING:  # avoid circular dependency
    from todolist.config import Settings  # coverage: ignore


class InMemoryTodoListRepository(AbstractTodoListRepository):
    items: list[TodoListItem] = []

    async def add(self, item: TodoListItem) -> None:
        self.items.append(item)

    async def list(self) -> Sequence[TodoListItem]:
        return self.items


class InMemoryUnitOfWork(AbstractUnitOfWork):
    todolist = InMemoryTodoListRepository()

    def __init__(self, settings: "Settings") -> None:
        """Create the unit of work, from the given configuration"""

    async def commit(self) -> None:
        """Commit the transation."""

    async def rollback(self) -> None:
        """Rollback the transation."""
