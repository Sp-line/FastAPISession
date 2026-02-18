from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import SeatType, SessionPriceLimits
from schemas.base import Id


class SessionPriceBase(BaseModel):
    seat_type: SeatType
    price: Annotated[int, Field(ge=SessionPriceLimits.PRICE_MIN)]


class SessionPriceBaseWithRelations(SessionPriceBase):
    session_id: Annotated[int, Field(ge=1)]


class SessionPriceCreateDB(SessionPriceBaseWithRelations):
    pass


class SessionPriceCreateReq(SessionPriceBaseWithRelations):
    pass


class SessionPriceUpdateBase(BaseModel):
    seat_type: SeatType | None = None
    price: Annotated[int | None, Field(ge=SessionPriceLimits.PRICE_MIN)] = None


class SessionPriceUpdateDB(SessionPriceUpdateBase):
    session_id: Annotated[int | None, Field(ge=1)] = None


class SessionPriceUpdateReq(SessionPriceUpdateBase):
    pass


class SessionPriceRead(Id, SessionPriceBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
