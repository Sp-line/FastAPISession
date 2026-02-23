from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Cinema
from integrity_handler import cinema_error_handler
from repositories.base import RepositoryBase
from schemas.cinema import CinemaCreateDB, CinemaUpdateDB


class CinemaRepository(
    RepositoryBase[
        Cinema,
        AsyncSession,
        CinemaCreateDB,
        CinemaUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Cinema,
            session=session,
            table_error_handler=cinema_error_handler,
        )
