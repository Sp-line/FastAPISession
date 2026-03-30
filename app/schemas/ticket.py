from pydantic import BaseModel, ConfigDict, PositiveInt

from constants import TicketStatus


class TicketEventBase(BaseModel):
    session_id: PositiveInt
    seat_id: PositiveInt

    model_config = ConfigDict(extra='ignore')


class TicketCreateEvent(TicketEventBase):
    status: TicketStatus

    model_config = ConfigDict(extra='ignore')


class TicketUpdateEvent(TicketEventBase):
    status: TicketStatus

    model_config = ConfigDict(extra='ignore')


class TicketDeleteEvent(TicketEventBase):
    model_config = ConfigDict(extra='ignore')
