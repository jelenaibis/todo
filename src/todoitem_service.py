from abc import ABC, abstractmethod
from src.schemas import TodoItem, UpdateTodoItem, BaseTodoItem, Message
from fastapi import status, HTTPException
from random import randint

todoitem_list = []


class ITODOItemsService(ABC):

    @abstractmethod
    def get_all_todoitems(self) -> list[TodoItem]:
        """Returns a list of all todoitems"""

    @abstractmethod
    def create_todoitem(self, todoitem: BaseTodoItem) -> TodoItem:
        """Creates new todoitem"""

    @abstractmethod
    def get_todoitem_by_id(self, id: int) -> TodoItem:
        """Creates new todoitem"""

    @abstractmethod
    def update_todoitem(self, id: int, new_data: UpdateTodoItem) -> TodoItem:
        """Updates a todoitem"""

    @abstractmethod
    def remove_todoitem(self, id: int) -> Message:
        """Removes a todoitem from list"""


class TODOService(ITODOItemsService):

    def get_all_todoitems(self) -> list[TodoItem]:
        return todoitem_list

    def update_todoitem(self, id: int, new_data: UpdateTodoItem) -> TodoItem:
        for todoitem in todoitem_list:
            if todoitem.id == id:
                if new_data is None:
                    raise ValueError(f"Todo with id {id} does not exist!")
                for field, value in new_data.model_dump().items():
                    if value is not None:
                        setattr(todoitem, field, value)
                return todoitem

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"TODOITEM with id {id} not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )

    @staticmethod
    def make_id():
        return len(todoitem_list) + 1

    def create_todoitem(self, todoitem: TodoItem) -> TodoItem:
        model = todoitem.model_dump()
        model.update({"id": self.make_id()})
        todoitem = TodoItem(**model)
        todoitem_list.append(todoitem)
        return todoitem

    def remove_todoitem(self, id: int) -> Message:
        for i, todo in enumerate(todoitem_list):
            if todo.id == id:
                todoitem = todoitem_list.pop(i)
                message_text = {"message": f"TODOITEM {todoitem.id} deleted successfully"}
                message = Message(**message_text)
                return message

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"TODOITEM [{id}] not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )

    def get_todoitem_by_id(self, id: int) -> TodoItem:
        for todoitem in todoitem_list:
            if todoitem.id == id:
                return todoitem

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"Todo [{id}] not found",
                "code": "TODO_NOT_FOUND",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )


def get_todoitem_service() -> ITODOItemsService:
    todo_service = TODOService()
    return todo_service
