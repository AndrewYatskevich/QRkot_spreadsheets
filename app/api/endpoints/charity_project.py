from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.api.validators import (
    check_charity_project_exists, check_fully_invested, check_invested
)
from app.core.user import current_superuser
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.services.investment import apply_donation
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectCreate, CharityProjectUpdate
)
from app.api.validators import check_name_duplicate

router = APIRouter()


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)
):
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        charity_project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    await check_name_duplicate(charity_project.name, session)
    charity_project = await charity_project_crud.create(
        charity_project, session
    )
    await apply_donation(session)
    await session.refresh(charity_project)

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    check_invested(charity_project)

    return await charity_project_crud.remove(
        charity_project, session
    )


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""
    charity_project = await check_charity_project_exists(project_id, session)
    check_fully_invested(charity_project)
    if obj_in.name:
        await check_name_duplicate(obj_in.name, session)

    return await charity_project_crud.update(
        charity_project, obj_in, session
    )
