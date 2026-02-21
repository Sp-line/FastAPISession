from pydantic import BaseModel, ConfigDict, PositiveInt

from constants import SeatAvailabilityStatus
from schemas.base import Id


class BookingBase(BaseModel):
    status: SeatAvailabilityStatus


class BookingBaseWithRelations(BookingBase):
    session_id: PositiveInt
    seat_id: PositiveInt


class BookingCreateDB(BookingBaseWithRelations):
    pass


class BookingCreateReq(BookingBaseWithRelations):
    pass


class BookingUpdateBase(BaseModel):
    status: SeatAvailabilityStatus | None = None


class BookingUpdateDB(BookingUpdateBase):
    session_id: PositiveInt | None = None
    seat_id: PositiveInt | None = None


class BookingUpdateReq(BookingUpdateBase):
    pass


class BookingRead(Id, BookingBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class BookingRelatedRead(Id, BookingBase):
    model_config = ConfigDict(from_attributes=True)
