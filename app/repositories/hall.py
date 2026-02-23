from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Hall, Seat
from integrity_handler import hall_error_handler
from repositories.base import RepositoryBase
from schemas.hall import HallCreateDB, HallUpdateDB


class HallRepository(
    RepositoryBase[
        Hall,
        AsyncSession,
        HallCreateDB,
        HallUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Hall,
            session=session,
            table_error_handler=hall_error_handler,
        )

    async def recalculate_and_update_capacity(self, *hall_ids: int) -> None:
        if not hall_ids:
            return

        count_subquery = (
            select(func.count(Seat.id))
            .where(Seat.hall_id == Hall.id)
            .correlate(Hall)
            .scalar_subquery()
        )

        stmt = (
            update(Hall)
            .where(Hall.id.in_(hall_ids))
            .values(capacity=count_subquery)
        )

        await self._session.execute(stmt)