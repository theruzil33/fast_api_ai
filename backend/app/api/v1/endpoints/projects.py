from enum import Enum

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.deps import get_current_user
from app.schemas.project import DataResponse, ProjectCreate, ProjectResponse, ok
from app.services import project_service

router = APIRouter(dependencies=[Depends(get_current_user)])

_VALID_SORT_FIELDS = {"name", "created_at"}


class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc"


@router.post("/", response_model=DataResponse[ProjectResponse], status_code=status.HTTP_201_CREATED)
async def create_project(data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = await project_service.create_project(data, db)
    return ok(project)


@router.get("/", response_model=DataResponse[list[ProjectResponse]])
async def list_projects(
    name: str | None = Query(default=None, description="Фильтр по названию (частичное совпадение)"),
    sort_by: str = Query(default="created_at", description="Поле сортировки: name, created_at"),
    order: SortOrder = Query(default=SortOrder.desc, description="Порядок сортировки: asc, desc"),
    db: AsyncSession = Depends(get_db),
):
    if sort_by not in _VALID_SORT_FIELDS:
        raise HTTPException(status_code=400, detail=f"sort_by must be one of: {', '.join(_VALID_SORT_FIELDS)}")
    projects = await project_service.list_projects(db, name=name, sort_by=sort_by, order=order)
    return ok(projects)


@router.get("/{project_id}", response_model=DataResponse[ProjectResponse])
async def get_project(project_id: int, db: AsyncSession = Depends(get_db)):
    project = await project_service.get_project(project_id, db)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return ok(project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await project_service.delete_project(project_id, db)
    if not deleted:
        raise HTTPException(status_code=404, detail="Project not found")
