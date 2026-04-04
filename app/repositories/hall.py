from typing import Sequence

from sqlalchemy import select, func, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Hall, Seat, OutboxEvent
from integrity_handler import hall_error_handler
from repositories.signals import SignalRepositoryBase
from schemas.base import Id
from schemas.hall import HallCreateDB, HallUpdateDB, HallCreateEvent, HallUpdateEvent, hall_event_schemas


class HallRepository(
    SignalRepositoryBase[
        Hall,
        HallCreateDB,
        HallUpdateDB,
        HallCreateEvent,
        HallUpdateEvent,
        Id
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Hall,
            session=session,
            table_error_handler=hall_error_handler,
            event_schemas=hall_event_schemas
        )

    async def _recalculate_capacity_in_db(self, *hall_ids: int) -> Sequence[Hall]:
        if not hall_ids:
            return []

        count_subquery = (
            select(func.count(Seat.id))
            .where(Seat.hall_id == Hall.id)
            .correlate(Hall)
            .scalar_subquery()
        )

        stmt = (
            update(Hall)
            .where(Hall.id.in_(hall_ids))
            .values(capacity=count_subquery)
            .returning(Hall)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def recalculate_and_update_capacity(self, *hall_ids: int) -> None:
        models = await self._recalculate_capacity_in_db(*hall_ids)
        if models:
            payloads = [
                self._event_schemas.update.model_validate(model).model_dump(mode="json")
                for model in models
            ]
            outbox_event = OutboxEvent(
                subject=self._topics.bulk_update,
                payload=payloads,
            )
            self._session.add(outbox_event)
