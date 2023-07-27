from tests.test_main import client


def test_get_all_empty_list():
    response = client.get("/todoitems/")
    assert response.status_code == 200
    assert response.json() == []


def test_get_all_todoitems():
    new_todoitem1 = {"name": "fastapi", "description": "Fastapi education"}
    client.post(
        "/todoitems/create/",
        json=new_todoitem1
    )

    new_todoitem2 = {"name": "django", "description": "Django education"}
    client.post(
        "/todoitems/create/",
        json=new_todoitem2
    )
    response = client.get("/todoitems/")
    assert response.status_code == 200
    assert len(response.json()) != 0
    assert isinstance(response.json(), list)


def test_create_todoitem_success():
    data = {"name": "fastapi", "description": "Fastapi education"}
    response = client.post(
        "/todoitems/create/",
        json=data
    )
    assert response.status_code == 200
    toditem = client.get("/todoitems/1")
    assert toditem.status_code == 200
    assert response.json() == {
        "id": 3,
        "name": "fastapi",
        "description": "Fastapi education"
    }


def test_create_todoitem_invalid_payload():
    data = {"description": "Description example"}
    response = client.post(
        "/todoitems/create/",
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
