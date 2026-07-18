import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_project(client: AsyncClient):
    payload = {"name": "My Test Project", "description": "A test project"}
    response = await client.post("/api/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "My Test Project"
    assert data["description"] == "A test project"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.asyncio
async def test_create_project_without_description(client: AsyncClient):
    payload = {"name": "Minimal Project"}
    response = await client.post("/api/projects", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Minimal Project"
    assert data["description"] is None


@pytest.mark.asyncio
async def test_list_projects(client: AsyncClient):
    await client.post("/api/projects", json={"name": "Project A"})
    await client.post("/api/projects", json={"name": "Project B"})

    response = await client.get("/api/projects")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    names = [p["name"] for p in data]
    assert "Project A" in names
    assert "Project B" in names


@pytest.mark.asyncio
async def test_get_project(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Get Test"})
    project_id = create_resp.json()["id"]

    response = await client.get(f"/api/projects/{project_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Get Test"
    assert data["id"] == project_id


@pytest.mark.asyncio
async def test_get_project_not_found(client: AsyncClient):
    response = await client.get("/api/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_project(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "Original"})
    project_id = create_resp.json()["id"]

    response = await client.patch(
        f"/api/projects/{project_id}", json={"name": "Updated", "description": "New desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"
    assert data["description"] == "New desc"


@pytest.mark.asyncio
async def test_delete_project(client: AsyncClient):
    create_resp = await client.post("/api/projects", json={"name": "To Delete"})
    project_id = create_resp.json()["id"]

    response = await client.delete(f"/api/projects/{project_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"/api/projects/{project_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_delete_project_not_found(client: AsyncClient):
    response = await client.delete("/api/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
