from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Seat
from integrity_handler import seat_error_handler
from repositories.base import RepositoryBase
from schemas.seat import SeatCreateDB, SeatUpdateDB


class SeatRepository(
    RepositoryBase[
        Seat,
        SeatCreateDB,
        SeatUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Seat,
            session=session,
            table_error_handler=seat_error_handler,
        )