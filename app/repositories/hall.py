from sqlalchemy import select, func, update

from core.models import Hall, Seat
from events.event_session import EventSession
from events.eventer import Eventer
from events.hall import hall_crud_publishers
from integrity_handler import hall_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.hall import HallCreateDB, HallUpdateDB, HallCreateEvent, HallUpdateEvent, hall_event_schemas


class HallRepository(
    SignalRepositoryBase[
        Hall,
        HallCreateDB,
        HallUpdateDB,
        HallCreateEvent,
        HallUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=Hall,
            session=session,
            table_error_handler=hall_error_handler,
            eventer=Eventer(hall_crud_publishers),
            event_schemas=hall_event_schemas
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
