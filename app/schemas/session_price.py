from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from constants import SeatType, SessionPriceLimits
from schemas.base import Id
from schemas.event import CRUDEventSchemas


class SessionPriceBase(BaseModel):
    seat_type: SeatType
    price: Annotated[Decimal, Field(ge=SessionPriceLimits.PRICE_MIN)]


class SessionPriceBaseWithRelations(SessionPriceBase):
    session_id: PositiveInt


class SessionPriceCreateReq(SessionPriceBaseWithRelations):
    pass


class SessionPriceCreateDB(SessionPriceCreateReq):
    pass


class SessionPriceUpdateBase(BaseModel):
    seat_type: SeatType | None = None
    price: Annotated[Decimal | None, Field(ge=SessionPriceLimits.PRICE_MIN)] = None


class SessionPriceUpdateReq(SessionPriceUpdateBase):
    pass


class SessionPriceUpdateDB(SessionPriceUpdateReq):
    session_id: PositiveInt | None = None


class SessionPriceRead(Id, SessionPriceBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class SessionPriceRelatedRead(Id, SessionPriceBase):
    model_config = ConfigDict(from_attributes=True)


class SessionPriceCreateEvent(SessionPriceRead):
    model_config = ConfigDict(from_attributes=True)


class SessionPriceUpdateEvent(SessionPriceRead):
    model_config = ConfigDict(from_attributes=True)


session_price_event_schemas = CRUDEventSchemas[
    SessionPriceCreateEvent,
    SessionPriceUpdateEvent,
    Id
](
    create=SessionPriceCreateEvent,
    update=SessionPriceUpdateEvent,
    delete=Id
)

