from pydantic import BaseModel, ConfigDict, PositiveInt

from constants import BookingStatus
from schemas.base import Id


class BookingBase(BaseModel):
    status: BookingStatus


class BookingBaseWithRelations(BookingBase):
    session_id: PositiveInt
    seat_id: PositiveInt


class BookingCreateReq(BookingBaseWithRelations):
    pass


class BookingCreateDB(BookingCreateReq):
    pass


class BookingUpdateBase(BaseModel):
    status: BookingStatus | None = None


class BookingUpdateReq(BookingUpdateBase):
    pass


class BookingUpdateDB(BookingUpdateReq):
    session_id: PositiveInt | None = None
    seat_id: PositiveInt | None = None


class BookingRead(Id, BookingBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class BookingRelatedRead(Id, BookingBase):
    model_config = ConfigDict(from_attributes=True)


class BookingDeleteDB(BaseModel):
    session_id: PositiveInt
    seat_id: PositiveInt
