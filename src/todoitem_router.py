from fastapi import APIRouter, Depends
from typing import List

from src.schemas import TODOItem, BaseTODOItem, UpdateTODOItem
from src.todoitem_service import get_todoitem_service

router = APIRouter(prefix="/todoitems", tags=["TODO ITEMS"])

#todoitems list for testing
todo_list = []


@router.get("/", response_model=List[TODOItem])
def get_all_todoitems(todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.get_all_todoitems()


@router.post("/create/", response_model=TODOItem)
async def create_todoitem(todoitem: BaseTODOItem, todoitem_service=Depends(get_todoitem_service)) -> TODOItem:
    return todoitem_service.create_todoitem(todoitem)


@router.delete("/{todo_id}", response_model=dict)
async def delete_todo(id: int, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.remove_todoitem(id)


@router.put("/{todo_id}", response_model=TODOItem)
async def update_todo(id: int, data: UpdateTODOItem, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.update_todoitem(id, data)


@router.get("/{todoitem_id}", response_model=TODOItem)
async def read_todoitem(id: int, todoitem_service=Depends(get_todoitem_service)):
    return todoitem_service.get_todoitem_by_id(id)
