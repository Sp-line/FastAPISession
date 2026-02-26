from core.models import SessionPrice
from events.event_session import EventSession
from events.eventer import Eventer
from events.session_price import session_price_crud_publishers
from integrity_handler import session_price_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.session_price import SessionPriceCreateDB, SessionPriceUpdateDB, session_price_event_schemas, \
    SessionPriceUpdateEvent, SessionPriceCreateEvent


class SessionPriceRepository(
    SignalRepositoryBase[
        SessionPrice,
        SessionPriceCreateDB,
        SessionPriceUpdateDB,
        SessionPriceCreateEvent,
        SessionPriceUpdateEvent,
        Id
    ]
):
    def __init__(self, session: EventSession) -> None:
        super().__init__(
            model=SessionPrice,
            session=session,
            table_error_handler=session_price_error_handler,
            eventer=Eventer(session_price_crud_publishers),
            event_schemas=session_price_event_schemas
        )
