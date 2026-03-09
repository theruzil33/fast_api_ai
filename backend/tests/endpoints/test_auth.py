from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.core.database import get_db
from app.core.security import create_access_token
from app.models.user import User

BASE_URL = "/api/v1/auth"


def make_user(username="admin", is_active=True) -> User:
    user = User()
    user.id = 1
    user.username = username
    user.hashed_password = "hashed_placeholder"
    user.is_active = is_active
    return user


def db_override(user: User | None):
    mock_db = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = user
    mock_db.execute.return_value = mock_result

    async def override():
        yield mock_db

    return override


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


# --- login ---

@pytest.mark.asyncio
@patch("app.api.v1.endpoints.auth.verify_password", return_value=True)
async def test_login_success(mock_verify, client):
    app.dependency_overrides[get_db] = db_override(make_user())

    response = await client.post(f"{BASE_URL}/login", json={"username": "admin", "password": "secret"})

    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"
    mock_verify.assert_called_once()


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.auth.verify_password", return_value=False)
async def test_login_wrong_password(mock_verify, client):
    app.dependency_overrides[get_db] = db_override(make_user())

    response = await client.post(f"{BASE_URL}/login", json={"username": "admin", "password": "wrong"})

    assert response.status_code == 401
    assert "error" in response.json()


@pytest.mark.asyncio
async def test_login_user_not_found(client):
    app.dependency_overrides[get_db] = db_override(None)

    response = await client.post(f"{BASE_URL}/login", json={"username": "nobody", "password": "any"})

    assert response.status_code == 401
    assert "error" in response.json()


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.auth.verify_password", return_value=True)
async def test_login_inactive_user(mock_verify, client):
    app.dependency_overrides[get_db] = db_override(make_user(is_active=False))

    response = await client.post(f"{BASE_URL}/login", json={"username": "admin", "password": "secret"})

    assert response.status_code == 403
    assert "error" in response.json()


# --- protected routes ---

@pytest.mark.asyncio
async def test_protected_route_without_token(client):
    response = await client.get("/api/v1/projects/")

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_protected_route_with_invalid_token(client):
    response = await client.get(
        "/api/v1/projects/",
        headers={"Authorization": "Bearer invalid.token.here"},
    )

    assert response.status_code == 401


@pytest.mark.asyncio
@patch("app.api.v1.endpoints.projects.project_service.list_projects", new_callable=AsyncMock)
async def test_protected_route_with_valid_token(mock_list, client):
    user = make_user()
    mock_list.return_value = []
    app.dependency_overrides[get_db] = db_override(user)

    token = create_access_token(user.username)

    response = await client.get(
        "/api/v1/projects/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
