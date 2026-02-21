from datetime import date, datetime, time, timezone, timedelta
from typing import Sequence

from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, load_only

from core.models import Movie, Session, Booking, Hall, SessionPrice
from integrity_handler import movie_error_handler
from repositories.base import RepositoryBase
from schemas.movie import MovieCreateDB, MovieUpdateDB


class MovieRepository(
    RepositoryBase[
        Movie,
        MovieCreateDB,
        MovieUpdateDB,
    ]
):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__(
            model=Movie,
            session=session,
            table_error_handler=movie_error_handler,
        )

    async def get_movies_with_relations_for_list_by_cinema_id_and_date(
            self,
            cinema_id: int,
            target_date: date,
            skip: int = 0,
            limit: int = 100
    ) -> Sequence[Movie]:
        start_of_day = datetime.combine(target_date, time.min, tzinfo=timezone.utc)
        start_of_next_day = start_of_day + timedelta(days=1)

        sold_out_stmt = (
            select(Session.id)
            .join(Booking, Booking.session_id == Session.id)
            .join(Hall, Hall.id == Session.hall_id)
            .where(
                Hall.cinema_id == cinema_id,
                Session.start_time >= start_of_day,
                Session.start_time < start_of_next_day
            )
            .group_by(Session.id, Hall.capacity)
            .having(func.count(Booking.id) >= Hall.capacity)
        )

        sold_out_result = await self._session.execute(sold_out_stmt)
        sold_out_session_ids = sold_out_result.scalars().all()

        conditions = [
            Session.start_time >= start_of_day,
            Session.start_time < start_of_next_day,
            Session.hall.has(Hall.cinema_id == cinema_id)
        ]

        if sold_out_session_ids:
            conditions.append(Session.id.notin_(sold_out_session_ids))

        session_condition = and_(*conditions)

        stmt = (
            select(self._model)
            .where(self._model.sessions.any(session_condition))
            .options(
                load_only(
                    self._model.id,
                    self._model.title,
                    self._model.age_rating,
                    self._model.poster_url
                ),
                selectinload(
                    self._model.sessions.and_(session_condition)
                )
                .options(
                    load_only(
                        Session.id,
                        Session.start_time,
                        Session.end_time,
                        Session.dimension_format,
                        Session.screen_technology,
                        Session.movie_id,
                        Session.hall_id
                    ),
                    selectinload(Session.hall).options(
                        load_only(
                            Hall.id,
                            Hall.name,
                            Hall.capacity
                        )
                    ),
                    selectinload(Session.prices).options(
                        load_only(
                            SessionPrice.id,
                            SessionPrice.seat_type,
                            SessionPrice.price,
                            SessionPrice.session_id
                        )
                    )
                )
            )
            .offset(skip)
            .limit(limit)
        )

        result = await self._session.execute(stmt)
        return result.scalars().all()
