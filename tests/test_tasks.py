from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)


def test_create_invalid_task():

    response = client.post(
        "/task",
        json={
            "name": "Invalid Task",
            "description": "Invalid Description",
            "priority": "invalid_priority",
            "status": "pending",
            "active": True
        }
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["loc"] == ["body", "priority"]


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


def test_create_task_with_parent():

    response_parent = client.post(
        "/task",
        json={
            "name": "Parent Task",
            "description": "Parent Description",
            "priority": "medium",
            "status": "in_progress",
            "active": True
        }
    )

    assert response_parent.status_code == 200

    parent_id = response_parent.json()["id"]

    response_child = client.post(
        "/task",
        json={
            "name": "Child Task",
            "description": "Child Description",
            "priority": "high",
            "status": "pending",
            "active": True,
            "parent_id": parent_id
        }
    )

    assert response_child.status_code == 200

    child_data = response_child.json()

    assert child_data["name"] == "Child Task"
    assert child_data["parent_id"] == parent_id


def test_parent_not_exist():

    response = client.post(
        "/task",
        json={
            "name": "Orphan Task",
            "description": "Orphan Description",
            "priority": "low",
            "status": "pending",
            "active": True,
            "parent_id": 999999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Parent task not found"


def test_same_parent():

    response_parent = client.post(
        "/task",
        json={
            "name": "Shared Parent Task",
            "description": "Shared Parent Description",
            "priority": "medium",
            "status": "in_progress",
            "active": True
        }
    )

    assert response_parent.status_code == 200

    parent_id = response_parent.json()["id"]

    response_child1 = client.post(
        "/task",
        json={
            "name": "Child Task 1",
            "description": "Child Description 1",
            "priority": "high",
            "status": "pending",
            "active": True,
            "parent_id": parent_id
        }
    )

    assert response_child1.status_code == 200

    response_child2 = client.post(
        "/task",
        json={
            "name": "Child Task 2",
            "description": "Child Description 2",
            "priority": "low",
            "status": "pending",
            "active": True,
            "parent_id": parent_id
        }
    )

    assert response_child2.status_code == 200


def test_duplicate_name():

    response1 = client.post(
        "/task",
        json={
            "name": "Duplicate Task",
            "description": "First Description",
            "priority": "medium",
            "status": "in_progress",
            "active": True
        }
    )

    assert response1.status_code == 200

    response2 = client.post(
        "/task",
        json={
            "name": "Duplicate Task",
            "description": "Second Description",
            "priority": "high",
            "status": "pending",
            "active": True
        }
    )

    assert response2.status_code == 200


def test_duplicate_name_with_parent():

    response_parent = client.post(
        "/task",
        json={
            "name": "Parent for Duplicate",
            "description": "Parent Description",
            "priority": "medium",
            "status": "in_progress",
            "active": True
        }
    )

    assert response_parent.status_code == 200

    parent_id = response_parent.json()["id"]

    response1 = client.post(
        "/task",
        json={
            "name": "Duplicate Child Task",
            "description": "First Child Description",
            "priority": "high",
            "status": "pending",
            "active": True,
            "parent_id": parent_id
        }
    )

    assert response1.status_code == 200

    response2 = client.post(
        "/task",
        json={
            "name": "Duplicate Child Task",
            "description": "Second Child Description",
            "priority": "low",
            "status": "pending",
            "active": True,
            "parent_id": parent_id
        }
    )

    assert response2.status_code == 200


def test_get_tasks():

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_task_not_found():

    response = client.get("/task/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Task not found"


def test_update_task():

    response = client.post(
        "/task",
        json={
            "name": "task",
            "description": "desc",
            "priority": "low",
            "status": "pending",
            "active": True
        }
    )

    assert response.status_code == 200

    task = response.json()

    update = client.put(
        f"/task/{task['id']}",
        json={
            "name": "updated",
            "description": "updated desc",
            "priority": "high",
            "status": "pending",
            "active": True
        }
    )

    assert update.status_code == 200

    data = update.json()

    assert data["name"] == "updated"


def test_delete_task():

    response_create = client.post(
        "/task",
        json={
            "name": "Task to Delete",
            "description": "Description of Task to Delete",
            "priority": "low",
            "status": "pending",
            "active": True
        }
    )

    assert response_create.status_code == 200

    task_id = response_create.json()["id"]

    response_delete = client.delete(f"/task/{task_id}")

    assert response_delete.status_code == 200

    deleted_data = response_delete.json()

    assert deleted_data["id"] == task_id

    response_get = client.get(f"/task/{task_id}")

    assert response_get.status_code == 404