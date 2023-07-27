from fastapi import APIRouter, Depends
from typing import List

from src.schemas import TodoItem, BaseTodoItem, UpdateTodoItem, Message
from src.todoitem_service import get_todoitem_service

router = APIRouter(prefix="/todoitems", tags=["TODO ITEMS"])


@router.get("/", response_model=List[TodoItem])
def get_all_todoitems(todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.get_all_todoitems()


@router.post("/create/", response_model=TodoItem)
async def create_todoitem(todoitem: BaseTodoItem, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.create_todoitem(todoitem)


@router.delete("/{todoitem_id}", response_model=Message)
async def delete_todo(todoitem_id: int, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.remove_todoitem(todoitem_id)


@router.put("/{todoitem_id}", response_model=TodoItem)
async def update_todo(todoitem_id: int, data: UpdateTodoItem, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.update_todoitem(todoitem_id, data)


@router.get("/{todoitem_id}", response_model=TodoItem)
async def read_todoitem(todoitem_id: int, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.get_todoitem_by_id(todoitem_id)
