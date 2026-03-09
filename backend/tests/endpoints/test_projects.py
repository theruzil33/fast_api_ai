from datetime import datetime, timezone
from unittest.mock import AsyncMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.deps import get_current_user
from app.models.project import Project
from app.models.user import User

BASE_URL = "/api/v1/projects"


def make_project(id=1, name="Test", description="Desc", created_at=None) -> Project:
    project = Project(id=id, name=name, description=description)
    project.created_at = created_at or datetime(2024, 1, 1, tzinfo=timezone.utc)
    return project


def mock_user() -> User:
    user = User()
    user.id = 1
    user.username = "testuser"
    user.hashed_password = "x"
    user.is_active = True
    return user


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_current_user] = mock_user
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.pop(get_current_user, None)


# --- create ---

@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.create_project", new_callable=AsyncMock)
async def test_create_project(mock_create, client):
    mock_create.return_value = make_project(name="Test", description="Desc")

    response = await client.post(f"{BASE_URL}/", json={"name": "Test", "description": "Desc"})

    assert response.status_code == 201
    data = response.json()["data"]
    assert data["name"] == "Test"
    assert data["description"] == "Desc"
    mock_create.assert_called_once()


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.create_project", new_callable=AsyncMock)
async def test_create_project_without_description(mock_create, client):
    mock_create.return_value = make_project(description=None)

    response = await client.post(f"{BASE_URL}/", json={"name": "No desc"})

    assert response.status_code == 201
    assert response.json()["data"]["description"] is None


# --- list ---

@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_list_projects_empty(mock_list, client):
    mock_list.return_value = []

    response = await client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert response.json()["data"] == []


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_list_projects(mock_list, client):
    mock_list.return_value = [make_project(id=1, name="A"), make_project(id=2, name="B")]

    response = await client.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_list_projects_filter_by_name(mock_list, client):
    mock_list.return_value = [make_project(name="Alpha project"), make_project(id=2, name="Beta project")]

    response = await client.get(f"{BASE_URL}/", params={"name": "project"})

    assert response.status_code == 200
    mock_list.assert_called_once_with(mock_list.call_args[0][0], name="project", sort_by="created_at", order="desc")


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_list_projects_sort_by_name_asc(mock_list, client):
    mock_list.return_value = [make_project(name="Alice"), make_project(id=2, name="Bob")]

    response = await client.get(f"{BASE_URL}/", params={"sort_by": "name", "order": "asc"})

    assert response.status_code == 200
    mock_list.assert_called_once_with(mock_list.call_args[0][0], name=None, sort_by="name", order="asc")


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_list_projects_sort_by_name_desc(mock_list, client):
    mock_list.return_value = [make_project(name="Bob"), make_project(id=2, name="Alice")]

    response = await client.get(f"{BASE_URL}/", params={"sort_by": "name", "order": "desc"})

    assert response.status_code == 200
    mock_list.assert_called_once_with(mock_list.call_args[0][0], name=None, sort_by="name", order="desc")


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_list_projects_sort_invalid_field(mock_list, client):
    response = await client.get(f"{BASE_URL}/", params={"sort_by": "unknown"})

    assert response.status_code == 400
    mock_list.assert_not_called()


# --- get ---

@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.get_project", new_callable=AsyncMock)
async def test_get_project(mock_get, client):
    mock_get.return_value = make_project(id=1)

    response = await client.get(f"{BASE_URL}/1")

    assert response.status_code == 200
    assert response.json()["data"]["id"] == 1


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.get_project", new_callable=AsyncMock)
async def test_get_project_not_found(mock_get, client):
    mock_get.return_value = None

    response = await client.get(f"{BASE_URL}/9999")

    assert response.status_code == 404


# --- delete ---

@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.delete_project", new_callable=AsyncMock)
async def test_delete_project(mock_delete, client):
    mock_delete.return_value = True

    response = await client.delete(f"{BASE_URL}/1")

    assert response.status_code == 204
    mock_delete.assert_called_once()


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.delete_project", new_callable=AsyncMock)
async def test_delete_project_not_found(mock_delete, client):
    mock_delete.return_value = False

    response = await client.delete(f"{BASE_URL}/9999")

    assert response.status_code == 404
