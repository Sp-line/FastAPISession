from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from constants import HallLimits, HallTechType
from schemas.base import Id


class HallBase(BaseModel):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    description: str | None = None
    tech_type: HallTechType


class HallBaseWithRelations(HallBase):
    cinema_id: PositiveInt


class HallCreateDB(HallBaseWithRelations):
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)] = 0


class HallCreateReq(HallBaseWithRelations):
    pass


class HallUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    description: str | None = None
    tech_type: HallTechType | None = None


class HallUpdateDB(HallUpdateBase):
    slug: Annotated[str | None, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)] = None
    capacity: Annotated[int | None, Field(ge=HallLimits.CAPACITY_MIN)] = None
    cinema_id: PositiveInt | None = None


class HallUpdateReq(HallUpdateBase):
    pass


class HallRead(Id, HallBaseWithRelations):
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)]

    model_config = ConfigDict(from_attributes=True)
