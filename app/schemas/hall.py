from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from constants import HallLimits, HallTechType
from schemas.base import Id
from schemas.cinema import CinemaReadWithRelationsForSession
from schemas.event import CRUDEventSchemas
from schemas.seat import SeatReadWithRelationsForSession


class HallBase(BaseModel):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    description: str | None = None
    tech_type: HallTechType


class HallBaseWithRelations(HallBase):
    cinema_id: PositiveInt


class HallCreateReq(HallBaseWithRelations):
    pass


class HallCreateDB(HallCreateReq):
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)] = 0


class HallUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    description: str | None = None
    tech_type: HallTechType | None = None


class HallUpdateReq(HallUpdateBase):
    pass


class HallUpdateDB(HallUpdateReq):
    slug: Annotated[str | None, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)] = None
    capacity: Annotated[int | None, Field(ge=HallLimits.CAPACITY_MIN)] = None
    cinema_id: PositiveInt | None = None


class HallRead(Id, HallBaseWithRelations):
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)]

    model_config = ConfigDict(from_attributes=True)


class HallRelatedReadForMovie(Id, BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)]


class HallRelatedReadForSession(HallRelatedReadForMovie):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    cinema: CinemaReadWithRelationsForSession
    seats: Annotated[list[SeatReadWithRelationsForSession], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class HallCreateEvent(HallRead):
    model_config = ConfigDict(from_attributes=True)


class HallUpdateEvent(HallRead):
    model_config = ConfigDict(from_attributes=True)


hall_event_schemas = CRUDEventSchemas[
    HallCreateEvent,
    HallUpdateEvent,
    Id
](
    create=HallCreateEvent,
    update=HallUpdateEvent,
    delete=Id
)

