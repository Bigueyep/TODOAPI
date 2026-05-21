from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_root():

    response = client.post("/task/")

    assert response.status_code == 200

    assert response.json() == {
        "message": "BDD ok"
    }


def test_create_task():

    response = client.post(
        "/task",
        json={
            "name": "Test Task",
            "description": "Test Description",
            "priority": "low",
            "status": "pending",
            "active": True
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Test Task"
    assert data["priority"] == "low"


def test_get_tasks():

    response = client.get("/tasks")

    assert response.status_code == 200

    assert isinstance(response.json(), list)


def test_get_task_not_found():

    response = client.get("/task/999999")

    assert response.status_code == 404

    assert response.json()["detail"] == "Task not found"