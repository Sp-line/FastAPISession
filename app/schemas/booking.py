from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import SeatAvailabilityStatus
from schemas.base import Id


class BookingBase(BaseModel):
    status: SeatAvailabilityStatus


class BookingBaseWithRelations(BookingBase):
    session_id: Annotated[int, Field(ge=1)]
    seat_id: Annotated[int, Field(ge=1)]


class BookingCreateDB(BookingBaseWithRelations):
    pass


class BookingCreateReq(BookingBaseWithRelations):
    pass


class BookingUpdateBase(BaseModel):
    status: SeatAvailabilityStatus | None = None


class BookingUpdateDB(BookingUpdateBase):
    session_id: Annotated[int | None, Field(ge=1)] = None
    seat_id: Annotated[int | None, Field(ge=1)] = None


class BookingUpdateReq(BookingUpdateBase):
    pass


class BookingRead(Id, BookingBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
