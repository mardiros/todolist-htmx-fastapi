from todolist.adapters.repositories import InMemoryTodoListRepository
from todolist.domain.model import TodoListItem


async def test_inmemorytodolist_repository():
    repo = InMemoryTodoListRepository()
    await repo.add(TodoListItem(label="Build the package"))
    assert await repo.list() == [TodoListItem(label="Build the package")]
