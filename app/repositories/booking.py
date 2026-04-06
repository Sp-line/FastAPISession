from collections.abc import Iterable
from typing import Sequence

from sqlalchemy import delete, tuple_
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Booking
from repositories.integrity_handler import booking_error_handler
from repositories.base import RepositoryBase
from schemas.booking import BookingCreateDB, BookingUpdateDB, BookingDeleteDB


class BookingRepository(
    RepositoryBase[
        Booking,
        AsyncSession,
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

    async def upsert_status(self, data: BookingCreateDB) -> Booking:
        stmt = insert(self._model).values(**data.model_dump())
        on_conflict_do_update_stmt = stmt.on_conflict_do_update(
            constraint="uq_bookings_session_id_seat_id",
            set_=dict(status=stmt.excluded.status)
        ).returning(self._model)

        try:
            result = await self._session.execute(on_conflict_do_update_stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.scalar_one()

    async def bulk_upsert_status(self, data: Iterable[BookingCreateDB]) -> Sequence[Booking]:
        values = [item.model_dump() for item in data]

        if not values:
            return []

        stmt = insert(self._model).values(values)
        on_conflict_do_update_stmt = stmt.on_conflict_do_update(
            constraint="uq_bookings_session_id_seat_id",
            set_=dict(status=stmt.excluded.status)
        ).returning(self._model)

        try:
            result = await self._session.execute(on_conflict_do_update_stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.scalars().all()

    async def delete_by_session_and_seat(self, data: BookingDeleteDB) -> bool:
        stmt = delete(self._model).where(
            self._model.session_id == data.session_id,
            self._model.seat_id == data.seat_id
        )

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.rowcount > 0  # type: ignore

    async def bulk_delete_by_session_and_seat(self, data: Iterable[BookingDeleteDB]) -> bool:
        keys_to_delete = [(item.session_id, item.seat_id) for item in data]

        if not keys_to_delete:
            return True

        stmt = delete(self._model).where(
            tuple_(self._model.session_id, self._model.seat_id).in_(keys_to_delete)
        )

        try:
            result = await self._session.execute(stmt)
        except IntegrityError as e:
            self._table_error_handler.handle(e)
            raise

        return result.rowcount == len(keys_to_delete) # type: ignore
