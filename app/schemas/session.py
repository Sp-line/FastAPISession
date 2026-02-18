from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import DimensionFormat, ScreenTechnology
from schemas.base import Id


class SessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    dimension_format: DimensionFormat
    screen_technology: ScreenTechnology
    is_active: bool = True


class SessionBaseWithRelations(SessionBase):
    hall_id: Annotated[int, Field(ge=1)]
    movie_id: Annotated[int, Field(ge=1)]


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
    hall_id: Annotated[int | None, Field(ge=1)] = None
    movie_id: Annotated[int | None, Field(ge=1)] = None


class SessionUpdateReq(SessionUpdateBase):
    pass


class SessionRead(Id, SessionBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
