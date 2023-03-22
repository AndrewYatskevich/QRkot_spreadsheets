from datetime import timedelta
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> list[dict[str, Union[str, timedelta]]]:
        projects = await session.execute(
            select([
                CharityProject.name,
                CharityProject.fundraising_time,
                CharityProject.description
            ]).where(
                CharityProject.fully_invested.is_(True)
            ).order_by(CharityProject.fundraising_time)
        )
        return projects.all()


charity_project_crud = CRUDCharityProject(CharityProject)
