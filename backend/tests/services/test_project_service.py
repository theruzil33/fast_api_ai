import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.database import Base
from app.models import Project  # noqa: F401 — register model
from app.schemas.project import ProjectCreate
from app.services import project_service

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db() -> AsyncSession:
    async with TestSessionLocal() as session:
        yield session


# --- create_project ---

@pytest.mark.asyncio
async def test_create_project(db):
    data = ProjectCreate(name="My project", description="Some desc")
    project = await project_service.create_project(data, db)

    assert project.id is not None
    assert project.name == "My project"
    assert project.description == "Some desc"
    assert project.created_at is not None


@pytest.mark.asyncio
async def test_create_project_without_description(db):
    data = ProjectCreate(name="No desc")
    project = await project_service.create_project(data, db)

    assert project.description is None


# --- list_projects ---

@pytest.mark.asyncio
async def test_list_projects_empty(db):
    result = await project_service.list_projects(db)
    assert result == []


@pytest.mark.asyncio
async def test_list_projects_returns_all(db):
    await project_service.create_project(ProjectCreate(name="A"), db)
    await project_service.create_project(ProjectCreate(name="B"), db)

    result = await project_service.list_projects(db)
    assert len(result) == 2


@pytest.mark.asyncio
async def test_list_projects_filter_by_name(db):
    await project_service.create_project(ProjectCreate(name="Alpha project"), db)
    await project_service.create_project(ProjectCreate(name="Beta project"), db)
    await project_service.create_project(ProjectCreate(name="Gamma"), db)

    result = await project_service.list_projects(db, name="project")
    names = [p.name for p in result]

    assert "Alpha project" in names
    assert "Beta project" in names
    assert "Gamma" not in names


@pytest.mark.asyncio
async def test_list_projects_filter_case_insensitive(db):
    await project_service.create_project(ProjectCreate(name="My Project"), db)

    result = await project_service.list_projects(db, name="my")
    assert len(result) == 1


@pytest.mark.asyncio
async def test_list_projects_filter_no_match(db):
    await project_service.create_project(ProjectCreate(name="Something"), db)

    result = await project_service.list_projects(db, name="xyz")
    assert result == []


@pytest.mark.asyncio
async def test_list_projects_sort_by_name_asc(db):
    for name in ("Charlie", "Alice", "Bob"):
        await project_service.create_project(ProjectCreate(name=name), db)

    result = await project_service.list_projects(db, sort_by="name", order="asc")
    names = [p.name for p in result]
    assert names == sorted(names)


@pytest.mark.asyncio
async def test_list_projects_sort_by_name_desc(db):
    for name in ("Charlie", "Alice", "Bob"):
        await project_service.create_project(ProjectCreate(name=name), db)

    result = await project_service.list_projects(db, sort_by="name", order="desc")
    names = [p.name for p in result]
    assert names == sorted(names, reverse=True)


# --- get_project ---

@pytest.mark.asyncio
async def test_get_project(db):
    created = await project_service.create_project(ProjectCreate(name="Get me"), db)

    result = await project_service.get_project(created.id, db)
    assert result is not None
    assert result.id == created.id
    assert result.name == "Get me"


@pytest.mark.asyncio
async def test_get_project_not_found(db):
    result = await project_service.get_project(9999, db)
    assert result is None


# --- delete_project ---

@pytest.mark.asyncio
async def test_delete_project(db):
    created = await project_service.create_project(ProjectCreate(name="Delete me"), db)

    deleted = await project_service.delete_project(created.id, db)
    assert deleted is True

    result = await project_service.get_project(created.id, db)
    assert result is None


@pytest.mark.asyncio
async def test_delete_project_not_found(db):
    deleted = await project_service.delete_project(9999, db)
    assert deleted is False
