from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import HallLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Cinema, Seat, Session


class Hall(IntIdPkMixin, Base):
    __table_args__ = (
        UniqueConstraint("cinema_id", "name", name="uq_halls_cinema_id_name"),
    )

    name: Mapped[str] = mapped_column(String(HallLimits.NAME_MAX))
    slug: Mapped[str] = mapped_column(String(HallLimits.SLUG_MAX), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    capacity: Mapped[int] = mapped_column(Integer, default=0)
    tech_type: Mapped[str] = mapped_column(String(HallLimits.TECH_TYPE_MAX))
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id", ondelete="RESTRICT"))

    cinema: Mapped["Cinema"] = relationship(back_populates="halls")
    seats: Mapped[list["Seat"]] = relationship(back_populates="hall", cascade="all, delete-orphan")
    sessions: Mapped[list["Session"]] = relationship(back_populates="hall", cascade="all, delete-orphan")