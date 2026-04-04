from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SessionPrice
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
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=SessionPrice,
            session=session,
            table_error_handler=session_price_error_handler,
            event_schemas=session_price_event_schemas
        )
