from abc import ABC, abstractmethod
from src.schemas import TODOItem, UpdateTODOItem, BaseTODOItem
from fastapi import Response, status, HTTPException


class ITODOItemsService(ABC):

    @abstractmethod
    def get_all_todoitems(self) -> list[TODOItem]:
        """Returns a list of all todoitems"""

    @abstractmethod
    def create_todoitem(self, todoitem: BaseTODOItem) -> TODOItem:
        """Creates new todoitem"""

    @abstractmethod
    def get_todoitem_by_id(self, id: int) -> TODOItem:
        """Creates new todoitem"""

    @abstractmethod
    def update_todoitem(self, id: int, new_data: UpdateTODOItem) -> TODOItem:
        """Updates a todoitem"""

    @abstractmethod
    def remove_todoitem(self, id: int) -> None:
        """Removes a todoitem from list"""


todoitem_list = []


class TODOService(ITODOItemsService):

    def get_all_todoitems(self) -> list[TODOItem]:
        """Returns a list of all todoitems"""
        return todoitem_list

    def update_todoitem(self, id: int, new_data: UpdateTODOItem) -> TODOItem:
        for todoitem in todoitem_list:
            if todoitem.id == id:
                if new_data is None:
                    raise ValueError(f"TODOITEM with id {id} does not exist!")
                for field, value in new_data.model_dump().items():
                    if value is not None:
                        setattr(todoitem, field, value)
                        return todoitem

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"TODOITEM [{id}] not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )

    def create_todoitem(self, todoitem: TODOItem) -> TODOItem:
        from random import randint
        model = todoitem.model_dump()
        model.update({"id": randint(0, 10)})
        todoitem = TODOItem(**model)
        todoitem_list.append(todoitem)
        return todoitem

    def remove_todoitem(self, id: int) -> dict:
        for i, todo in enumerate(todoitem_list):
            if todo.id == id:
                todoitem = todoitem_list.pop(i)
                return {"message": f"TODOITEM {todoitem} deleted successfully"}

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "message": f"TODOITEM [{id}] not found",
                "status_code": status.HTTP_404_NOT_FOUND
            }
        )

    def get_todoitem_by_id(self, id: int) -> TODOItem:
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
