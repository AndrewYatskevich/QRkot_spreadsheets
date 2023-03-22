from sqlalchemy import Column, Integer, ForeignKey, Text

from app.models.base import CharityProjectDonation


class Donation(CharityProjectDonation):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text)
