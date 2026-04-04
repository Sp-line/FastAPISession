from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Seat
from integrity_handler import seat_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.seat import SeatCreateDB, SeatUpdateDB, SeatCreateEvent, SeatUpdateEvent, seat_event_schemas, \
    SeatDeleteEvent


class SeatRepository(
    SignalRepositoryBase[
        Seat,
        SeatCreateDB,
        SeatUpdateDB,
        SeatCreateEvent,
        SeatUpdateEvent,
        SeatDeleteEvent,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Seat,
            session=session,
            table_error_handler=seat_error_handler,
            event_schemas=seat_event_schemas
        )
