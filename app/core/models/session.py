from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func, column, true, CheckConstraint
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import SessionLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Hall, Movie, SessionPrice, Booking


class Session(IntIdPkMixin, Base):
    __table_args__ = (
        ExcludeConstraint(
            ("hall_id", "="),
            (
                func.tstzrange(
                    column("start_time"),
                    column("end_time"),
                    "[)"
                ),
                "&&"
            ),
            where=(
                    column("is_active") == true()
            ),
            name="excl_session_hall_time_overlap",
            using="gist"
        ),
        CheckConstraint(
            "end_time > start_time",
            name="ck_sessions_end_time_after_start_time"
        ),
    )

    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    dimension_format: Mapped[str] = mapped_column(String(SessionLimits.DIMENSION_FORMAT_MAX))
    screen_technology: Mapped[str] = mapped_column(String(SessionLimits.SCREEN_TECHNOLOGY_MAX))

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id", ondelete="RESTRICT"), index=True)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id", ondelete="RESTRICT"), index=True)

    hall: Mapped["Hall"] = relationship(back_populates="sessions")
    movie: Mapped["Movie"] = relationship(back_populates="sessions")

    prices: Mapped[list["SessionPrice"]] = relationship(back_populates="session", cascade="all, delete-orphan")
    bookings: Mapped[list["Booking"]] = relationship(back_populates="session")
