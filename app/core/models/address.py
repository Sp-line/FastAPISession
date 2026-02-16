from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from constants import AddressLimits
from core.models import Base
from core.models.mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from core.models import Cinema


class Address(IntIdPkMixin, Base):
    __tablename__ = "addresses"

    __table_args__ = (
        CheckConstraint(
            f"latitude >= {AddressLimits.LATITUDE_MIN} AND latitude <= {AddressLimits.LATITUDE_MAX}",
            name="check_latitude_range"
        ),
        CheckConstraint(
            f"longitude >= {AddressLimits.LONGITUDE_MIN} AND longitude <= {AddressLimits.LONGITUDE_MAX}",
            name="check_longitude_range"
        ),
    )

    city: Mapped[str] = mapped_column(String(AddressLimits.CITY_MAX))
    street: Mapped[str] = mapped_column(String(AddressLimits.STREET_MAX))
    house_number: Mapped[str] = mapped_column(String(AddressLimits.HOUSE_NUMBER_MAX))
    zip_code: Mapped[str] = mapped_column(String(AddressLimits.ZIP_CODE_MAX))

    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)

    cinema_id: Mapped[int] = mapped_column(ForeignKey('cinemas.id', ondelete='CASCADE'), unique=True)

    cinema: Mapped["Cinema"] = relationship(back_populates="address")
