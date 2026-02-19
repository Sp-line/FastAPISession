from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Booking
from integrity_handler import booking_error_handler
from repositories.base import RepositoryBase
from schemas.booking import BookingCreateDB, BookingUpdateDB


class BookingRepository(
    RepositoryBase[
        Booking,
        BookingCreateDB,
        BookingUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Booking,
            session=session,
            table_error_handler=booking_error_handler,
        )
