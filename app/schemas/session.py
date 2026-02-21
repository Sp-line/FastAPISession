from datetime import datetime
from typing import Annotated, Self

from pydantic import BaseModel, Field, ConfigDict, PositiveInt, model_validator

from constants import DimensionFormat, ScreenTechnology, MovieLimits, ImageUrlLimits
from constants.movie import AgeRating
from schemas.base import Id
from schemas.hall import HallRelatedReadForMovie, HallRelatedReadForSession
from schemas.session_price import SessionPriceRelatedRead


class SessionBase(BaseModel):
    start_time: datetime
    end_time: datetime
    dimension_format: DimensionFormat
    screen_technology: ScreenTechnology

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


class SessionUpdateDB(SessionUpdateBase):
    hall_id: PositiveInt | None = None
    movie_id: PositiveInt | None = None


class SessionUpdateReq(SessionUpdateBase):
    pass


class SessionRead(Id, SessionBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)


class SessionRelatedReadWithRelationsForMovie(Id, SessionBase):
    hall: HallRelatedReadForMovie
    prices: Annotated[list[SessionPriceRelatedRead], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)


class MovieRelatedReadForSession(Id):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    duration: Annotated[int, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)]
    age_rating: AgeRating
    poster_url: Annotated[str, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)]

    model_config = ConfigDict(from_attributes=True)


class SessionDetail(Id, SessionBase):
    prices: Annotated[list[SessionPriceRelatedRead], Field(default_factory=list)]
    movie: MovieRelatedReadForSession
    hall: HallRelatedReadForSession


    model_config = ConfigDict(from_attributes=True)

