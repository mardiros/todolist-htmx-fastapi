
from todolist.adapters.repositories import InMemoryTodoListRepository
from todolist.domain.model import TodoListItem


def test_inmemorytodolist_repository():
    repo = InMemoryTodoListRepository()
    repo.add(TodoListItem(label="Build the package"))
    assert repo.list() == [TodoListItem(label="Build the package")]


