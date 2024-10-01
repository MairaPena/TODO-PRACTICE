from fastapi.testclient import TestClient
from app import main

client = TestClient(main.app)


def test_should_create_task_when_calling_create_task_endpoint():
    # configurations
    task = {"title": "Task1", "description": "This is a short task"}
    # action
    response = client.post("/create_task", json=task)
    response_obj = main.Response(**response.json())

    # assertion
    assert response.status_code == 201
    assert isinstance(response_obj.task_id, str)


def test_should_get_all_tasks_when_calling_get_all_task_endpoint():
    # configurations
    task = {"title": "Task1", "description": "This is a short task"}
    task2 = {"title": "task2", "description": "This a short description"}
    client.post("/create_task", json=task)
    client.post("/create_task", json=task2)

    # action
    response = client.get("/get_all_tasks")

    # assertion
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


def test_should_get_task_by_id_when_calling_get_task_by_id_endpoint():
    # configurations
    task = {"title": "title1", "description": "This is a description"}
    response1 = client.post("/create_task", json=task)
    id_ = response1.json()["task_id"]
    # action
    response = client.get(f"/get_task_by_id/{id_}")

    # assert
    assert response.json()["id"] == id_
