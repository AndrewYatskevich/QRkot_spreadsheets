from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.user import current_superuser, current_user
from app.core.db import get_async_session
from app.crud.donation import donation_crud
from app.services.investment import apply_donation
from app.models import User
from app.schemas.donation import (
    DonationDB, DonationShortDB, DonationCreate
)

router = APIRouter()


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationShortDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    return await donation_crud.get_by_user(user, session)


@router.post(
    '/',
    response_model=DonationShortDB,
    response_model_exclude_none=True,
)
async def create_new_donation(
        donation: DonationCreate,
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session)
):
    donation = await donation_crud.create(
        donation, session, user
    )
    await apply_donation(session)
    await session.refresh(donation)
    return donation
