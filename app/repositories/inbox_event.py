from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import InboxEvent
from repositories import RepositoryBase
from repositories.integrity_handler import inbox_events_error_handler
from schemas.inbox_event import InboxEventCreateDB, InboxEventUpdateDB


class InboxEventRepository(
    RepositoryBase[
        InboxEvent,
        AsyncSession,
        InboxEventCreateDB,
        InboxEventUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=InboxEvent,
            session=session,
            table_error_handler=inbox_events_error_handler,
        )

    async def add_if_not_exists(self, data: InboxEventCreateDB) -> bool:
        stmt = insert(self._model).values(data.model_dump())
        on_conflict_do_nothing_stmt = stmt.on_conflict_do_nothing(
            constraint="uq_inbox_events_code_handler"
        )

        try:
            result = await self._session.execute(on_conflict_do_nothing_stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.rowcount > 0  # type: ignore[attr-defined]
