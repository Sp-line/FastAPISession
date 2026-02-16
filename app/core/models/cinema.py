from typing import TYPE_CHECKING

from sqlalchemy import String, Text, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import CinemaLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Address
    from core.models import Hall


class Cinema(IntIdPkMixin, Base):
    name: Mapped[str] = mapped_column(String(CinemaLimits.NAME_MAX))
    slug: Mapped[str] = mapped_column(String(CinemaLimits.SLUG_MAX), unique=True)
    description: Mapped[str | None] = mapped_column(Text)
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)

    address: Mapped["Address"] = relationship(back_populates="cinema", uselist=False, cascade="all, delete-orphan")
    halls: Mapped[list["Hall"]] = relationship(back_populates="cinema", cascade="all, delete-orphan")