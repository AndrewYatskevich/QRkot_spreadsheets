from sqlalchemy import Column, String, Text

from app.models.base import CharityProjectDonation


class CharityProject(CharityProjectDonation):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)
