from todolist.adapters.repositories import InMemoryTodoListRepository
from todolist.domain.model import TodoListItem


async def test_inmemorytodolist_repository():
    repo = InMemoryTodoListRepository()
    await repo.add(TodoListItem(label="Build the package"))
    todo = await repo.list()
    assert todo == [TodoListItem(id=todo[0].id, label="Build the package")]
