from datetime import datetime
from sqlalchemy import Column, Integer, Boolean, DateTime, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


class CharityProjectDonation(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime, default=None)

    @property
    def remaining_amount(self):
        return self.full_amount - self.invested_amount

    @classmethod
    async def get_not_fully_invested(cls, session: AsyncSession):
        objs = await session.execute(
            select(cls).where(cls.fully_invested.is_(False))
        )
        return objs.scalars().all()

    def mark_as_fully_invested(self):
        self.invested_amount = self.full_amount
        self.fully_invested = True
        self.close_date = datetime.now()
