from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import CharityProjectDonation


class Donation(CharityProjectDonation):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)

    def __repr__(self):
        return (f'<Donation(user_id={self.user_id}, '
                f'full_amount={self.full_amount})>')
