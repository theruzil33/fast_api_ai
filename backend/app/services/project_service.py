from sqlalchemy import select, delete, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.project import Project
from app.schemas.project import ProjectCreate

_SORT_FIELDS = {"name": Project.name, "created_at": Project.created_at}


async def create_project(data: ProjectCreate, db: AsyncSession) -> Project:
    project = Project(name=data.name, description=data.description)
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project


async def list_projects(
    db: AsyncSession,
    name: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
) -> list[Project]:
    sort_col = _SORT_FIELDS[sort_by]
    ordering = asc(sort_col) if order == "asc" else desc(sort_col)

    query = select(Project).order_by(ordering)
    if name is not None:
        query = query.where(Project.name.ilike(f"%{name}%"))

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_project(project_id: int, db: AsyncSession) -> Project | None:
    return await db.get(Project, project_id)


async def delete_project(project_id: int, db: AsyncSession) -> bool:
    result = await db.execute(delete(Project).where(Project.id == project_id))
    await db.commit()
    return result.rowcount > 0
