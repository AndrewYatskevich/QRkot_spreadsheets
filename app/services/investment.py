from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def apply_donation(session: AsyncSession):
    projects = await CharityProject.get_not_fully_invested(session)
    donations = await Donation.get_not_fully_invested(session)

    while projects and donations:
        project = projects[0]
        donation = donations[0]

        donation_remaining_amount = donation.remaining_amount
        project_remaining_amount = project.remaining_amount

        if donation_remaining_amount > project_remaining_amount:
            project.mark_as_fully_invested()
            donation.invested_amount += project_remaining_amount
            projects.pop(0)
        elif donation_remaining_amount < project_remaining_amount:
            donation.mark_as_fully_invested()
            project.invested_amount += donation_remaining_amount
            donations.pop(0)
        else:
            project.mark_as_fully_invested()
            donation.mark_as_fully_invested()
            projects.pop(0)
            donations.pop(0)

        session.add_all([project, donation])

    await session.commit()
