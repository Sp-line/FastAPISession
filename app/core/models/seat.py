from typing import TYPE_CHECKING

from sqlalchemy import String, Integer, ForeignKey, UniqueConstraint, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import SeatLimits, SeatType
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Hall, Booking


class Seat(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint(
            "hall_id", "row_label", "column_label",
            name="uq_seats_hall_id_row_label_column_label"
        ),
        UniqueConstraint(
            "hall_id", "row", "column",
            name="uq_seats_hall_id_row_column"
        ),
    )

    type: Mapped[SeatType] = mapped_column(SAEnum(SeatType, native_enum=False, length=SeatLimits.TYPE_MAX))

    row_label: Mapped[str] = mapped_column(String(SeatLimits.ROW_LABEL_MAX))
    column_label: Mapped[str] = mapped_column(String(SeatLimits.COLUMN_LABEL_MAX))

    row: Mapped[int] = mapped_column(Integer)
    column: Mapped[int] = mapped_column(Integer)

    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id", ondelete="CASCADE"))

    hall: Mapped["Hall"] = relationship(back_populates="seats")

    bookings: Mapped[list["Booking"]] = relationship(back_populates="seat")
