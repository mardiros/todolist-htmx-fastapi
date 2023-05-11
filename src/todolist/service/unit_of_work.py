import abc
from types import TracebackType
from typing import TYPE_CHECKING, Optional, Type

from todolist.domain.repositories import AbstractTodoListRepository

if TYPE_CHECKING:  # avoid circular dependency
    from todolist.config import Settings  # coverage: ignore


class AbstractUnitOfWork(abc.ABC):
    todolist: AbstractTodoListRepository

    @abc.abstractmethod
    def __init__(self, settings: "Settings") -> None:
        """Create the unit of work, from the given configuration"""

    async def __aenter__(self) -> "AbstractUnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        """Rollback in case of exception."""
        if exc:
            await self.rollback()

    @abc.abstractmethod
    async def commit(self) -> None:
        """Commit the transation."""

    @abc.abstractmethod
    async def rollback(self) -> None:
        """Rollback the transation."""
