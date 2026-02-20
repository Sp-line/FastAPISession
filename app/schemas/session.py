from datetime import datetime
from typing import Annotated, Self

from pydantic import BaseModel, Field, ConfigDict, PositiveInt, model_validator

from constants import DimensionFormat, ScreenTechnology
from schemas.base import Id


class SessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    dimension_format: DimensionFormat
    screen_technology: ScreenTechnology
    is_active: bool = True

    @model_validator(mode='after')
    def check_end_time_after_start_time(self) -> Self:
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self


class SessionBaseWithRelations(SessionBase):
    hall_id: PositiveInt
    movie_id: PositiveInt


class SessionCreateDB(SessionBaseWithRelations):
    pass


class SessionCreateReq(SessionBaseWithRelations):
    pass


class SessionUpdateBase(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    dimension_format: DimensionFormat | None = None
    screen_technology: ScreenTechnology | None = None
    is_active: bool | None = None


class SessionUpdateDB(SessionUpdateBase):
    hall_id: PositiveInt | None = None
    movie_id: PositiveInt | None = None


class SessionUpdateReq(SessionUpdateBase):
    pass


class SessionRead(Id, SessionBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
