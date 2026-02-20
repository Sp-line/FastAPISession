from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from constants import SeatType, SessionPriceLimits
from schemas.base import Id


class SessionPriceBase(BaseModel):
    seat_type: SeatType
    price: Annotated[int, Field(ge=SessionPriceLimits.PRICE_MIN)]


class SessionPriceBaseWithRelations(SessionPriceBase):
    session_id: PositiveInt


class SessionPriceCreateDB(SessionPriceBaseWithRelations):
    pass


class SessionPriceCreateReq(SessionPriceBaseWithRelations):
    pass


class SessionPriceUpdateBase(BaseModel):
    seat_type: SeatType | None = None
    price: Annotated[Decimal | None, Field(ge=SessionPriceLimits.PRICE_MIN)] = None


class SessionPriceUpdateDB(SessionPriceUpdateBase):
    session_id: PositiveInt | None = None


class SessionPriceUpdateReq(SessionPriceUpdateBase):
    pass


class SessionPriceRead(Id, SessionPriceBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class SessionPriceRelatedRead(Id, SessionPriceBase):
    model_config = ConfigDict(from_attributes=True)
