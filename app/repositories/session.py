from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Session
from integrity_handler import session_error_handler
from repositories.base import RepositoryBase
from schemas.session import SessionCreateDB, SessionUpdateDB


class SessionRepository(
    RepositoryBase[
        Session,
        SessionCreateDB,
        SessionUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Session,
            session=session,
            table_error_handler=session_error_handler,
        )