from sqlalchemy.ext.asyncio import AsyncSession

from core.models import SessionPrice
from integrity_handler import session_price_error_handler
from repositories.base import RepositoryBase
from schemas.session_price import SessionPriceCreateDB, SessionPriceUpdateDB


class SessionPriceRepository(
    RepositoryBase[
        SessionPrice,
        AsyncSession,
        SessionPriceCreateDB,
        SessionPriceUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=SessionPrice,
            session=session,
            table_error_handler=session_price_error_handler,
        )
