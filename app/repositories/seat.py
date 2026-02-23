from core.models import Seat
from events.eventer import Eventer
from events.seat import seat_crud_publishers
from events.session import EventSession
from integrity_handler import seat_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.seat import SeatCreateDB, SeatUpdateDB, SeatCreateEvent, SeatUpdateEvent, seat_event_schemas


class SeatRepository(
    SignalRepositoryBase[
        Seat,
        SeatCreateDB,
        SeatUpdateDB,
        SeatCreateEvent,
        SeatUpdateEvent,
        Id,
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=Seat,
            session=session,
            table_error_handler=seat_error_handler,
            eventer=Eventer(publishers=seat_crud_publishers),
            event_schemas=seat_event_schemas
        )
