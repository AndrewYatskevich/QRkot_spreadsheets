from sqlalchemy import Column, Interval, String, Text

from app.models.base import CharityProjectDonation


class CharityProject(CharityProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
    fundraising_time = Column(Interval, default=None)

    def mark_as_fully_invested(self):
        super().mark_as_fully_invested()
        self.fundraising_time = self.close_date - self.create_date

    def __repr__(self):
        return (f'<CharityProject(name={self.name}, '
                f'full_amount={self.full_amount})>')
