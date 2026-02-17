from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import BookingLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Session, Seat


class Booking(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "session_id", "seat_id",
            name="uq_bookings_session_id_seat_id"
        ),
    )

    status: Mapped[str] = mapped_column(String(BookingLimits.STATUS_MAX))

    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id", ondelete="RESTRICT"))
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id", ondelete="RESTRICT"))

    session: Mapped["Session"] = relationship(back_populates="bookings")
    seat: Mapped["Seat"] = relationship(back_populates="bookings")
