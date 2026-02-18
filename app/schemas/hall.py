from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import HallLimits, HallTechType
from schemas.base import Id


class HallBase(BaseModel):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    slug: Annotated[str, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)]
    description: str | None = None
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)]
    tech_type: HallTechType


class HallBaseWithRelations(HallBase):
    cinema_id: Annotated[int, Field(ge=1)]


class HallCreateDB(HallBaseWithRelations):
    pass


class HallCreateReq(HallBase):
    name: Annotated[str, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)]
    description: str | None = None
    capacity: Annotated[int, Field(ge=HallLimits.CAPACITY_MIN)]
    tech_type: HallTechType


class HallUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    slug: Annotated[str | None, Field(min_length=HallLimits.SLUG_MIN, max_length=HallLimits.SLUG_MAX)] = None
    description: str | None = None
    capacity: Annotated[int | None, Field(ge=HallLimits.CAPACITY_MIN)] = None
    tech_type: HallTechType | None = None


class HallUpdateDB(HallUpdateBase):
    cinema_id: Annotated[int | None, Field(ge=1)] = None


class HallUpdateReq(BaseModel):
    name: Annotated[str | None, Field(min_length=HallLimits.NAME_MIN, max_length=HallLimits.NAME_MAX)] = None
    description: str | None = None
    tech_type: HallTechType | None = None


class HallRead(Id, HallBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
