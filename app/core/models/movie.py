from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, SmallInteger, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import MovieLimits, ImageUrlLimits, SlugLimits
from constants.movie import AgeRating
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Session


class Movie(IntIdPkMixin, Base):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=False)
    slug: Mapped[str] = mapped_column(String(SlugLimits.SLUG_MAX), unique=True)
    title: Mapped[str] = mapped_column(String(MovieLimits.TITLE_MAX))
    duration: Mapped[int] = mapped_column(SmallInteger)
    age_rating: Mapped[AgeRating] = mapped_column(SAEnum(AgeRating, native_enum=False, length=MovieLimits.AGE_RATING_MAX))
    premiere_date: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    poster_url: Mapped[str | None] = mapped_column(String(ImageUrlLimits.MAX))

    sessions: Mapped[list["Session"]] = relationship(back_populates="movie", cascade="all, delete-orphan")