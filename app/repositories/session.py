from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only, joinedload

from core.models import Session, Hall, Cinema, Seat, Booking, SessionPrice, Movie, Address
from integrity_handler import session_error_handler
from repositories.base import RepositoryBase
from schemas.session import SessionCreateDB, SessionUpdateDB


class SessionRepository(
    RepositoryBase[
        Session,
        AsyncSession,
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

    async def get_for_detail(self, session_id: int) -> Session | None:
        stmt = (
            select(Session)
            .where(Session.id == session_id)
            .options(
                load_only(
                    Session.id,
                    Session.start_time,
                    Session.end_time,
                    Session.dimension_format,
                    Session.screen_technology,
                ),
                joinedload(Session.movie).load_only(
                    Movie.id,
                    Movie.title,
                    Movie.duration,
                    Movie.age_rating,
                    Movie.poster_url
                ),
                selectinload(Session.prices).load_only(
                    SessionPrice.id,
                    SessionPrice.seat_type,
                    SessionPrice.price
                ),
                joinedload(Session.hall).options(
                    load_only(
                        Hall.id,
                        Hall.name,
                        Hall.capacity
                    ),
                    joinedload(Hall.cinema).options(
                        load_only(Cinema.id, Cinema.name),
                        joinedload(Cinema.address).load_only(
                            Address.id, Address.city, Address.street,
                            Address.house_number, Address.zip_code,
                            Address.latitude, Address.longitude
                        )
                    ),
                    selectinload(Hall.seats).options(
                        load_only(
                            Seat.id,
                            Seat.type,
                            Seat.row_label,
                            Seat.column_label,
                            Seat.row,
                            Seat.column
                        ),
                        selectinload(Seat.bookings.and_(Booking.session_id == session_id))
                        .load_only(Booking.id, Booking.status)
                    ),
                ),
            )
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()
