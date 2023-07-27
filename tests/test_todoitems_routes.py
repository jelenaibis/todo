from tests.conftest import client
from unittest.mock import patch
from src.schemas import TodoItem


def fake_todo_items_list():
    new_data1 = {"id": 1, "name": "fastapi", "description": "Fastapi education"}
    new_data2 = {"id": 2, "name": "django", "description": "Django education"}
    todo_item_1 = TodoItem(**new_data1)
    todo_item_2 = TodoItem(**new_data2)
    return [todo_item_1, todo_item_2]


def test_get_all_empty_list():
    response = client.get("/todoitems")
    assert response.status_code == 200
    assert response.json() == []


@patch("src.todoitem_service.TODOService.get_all_todoitems",
       return_value=fake_todo_items_list())
def test_get_all_todoitems(mocked):
    response = client.get("/todoitems")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) != 0
    assert response.json() == [
        {"id": 1, "name": "fastapi", "description": "Fastapi education"},
        {"id": 2, "name": "django", "description": "Django education"}
    ]


def test_create_todoitem_success():
    data = {"name": "fastapi", "description": "Fastapi education"}
    response = client.post(
        "/todoitems/create",
        json=data
    )
    assert response.status_code == 200
    toditem = client.get("/todoitems/1")
    assert toditem.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "fastapi",
        "description": "Fastapi education"
    }


def test_create_todoitem_invalid_payload():
    data = {"description": "Description example"}
    response = client.post(
        "/todoitems/create",
        json=data
    )
    assert response.status_code == 422


def test_read_todoitem_success():
    response = client.get("/todoitems/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "name": "fastapi",
        "description": "Fastapi education"
    }


def test_read_todoitem_invalid_id():
    response = client.get("/todoitems/-1")
    assert response.status_code == 404


def test_update_todo():
    new_name = "Java"
    new_decsription = "Java education"
    response = client.put("/todoitems/1", json={"name": new_name})
    assert response.status_code == 200
    assert response.json()["name"] == new_name
    response = client.put("/todoitems/1", json={"description": new_decsription})
    assert response.status_code == 200
    assert response.json()["description"] == new_decsription

    new_data = {
        "name": "Java + C#",
        "description": "Java + C# Education"
    }
    response = client.put("/todoitems/1", json=new_data)
    assert response.json()["name"] == new_data["name"]
    assert response.json()["description"] == new_data["description"]


def test_delete_todo():
    response = client.delete("/todoitems/1")
    assert response.status_code == 200
    assert response.json()["message"] == "TODOITEM 1 deleted successfully"
    company = client.get("/companies/1")
    assert company.status_code == 404
