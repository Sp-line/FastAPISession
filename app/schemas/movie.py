from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import MovieLimits, ImageUrlLimits
from constants.movie import AgeRating
from schemas.base import Id
from schemas.session import SessionRelatedReadWithRelationsForMovie


class MovieBase(BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    duration: Annotated[int, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)]
    age_rating: AgeRating
    premiere_date: datetime | None = None
    poster_url: Annotated[str, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)]


class MovieCreateDB(Id, MovieBase):
    slug: Annotated[str, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)]


class MovieCreateReq(Id, MovieBase):
    pass


class MovieUpdateBase(BaseModel):
    title: Annotated[str | None, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)] = None
    duration: Annotated[int | None, Field(ge=MovieLimits.DURATION_MIN, le=MovieLimits.DURATION_MAX)] = None
    age_rating: AgeRating | None = None
    premiere_date: datetime | None = None


class MovieUpdateDB(MovieUpdateBase):
    slug: Annotated[str | None, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)] = None
    poster_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None


class MovieUpdateReq(MovieUpdateBase):
    pass


class MovieRead(Id, MovieBase):
    slug: Annotated[str, Field(min_length=MovieLimits.SLUG_MIN, max_length=MovieLimits.SLUG_MAX)]

    model_config = ConfigDict(from_attributes=True)


class MovieRelationsRead(Id, BaseModel):
    title: Annotated[str, Field(min_length=MovieLimits.TITLE_MIN, max_length=MovieLimits.TITLE_MAX)]
    age_rating: AgeRating
    poster_url: Annotated[str | None, Field(min_length=ImageUrlLimits.MIN, max_length=ImageUrlLimits.MAX)] = None
    sessions: Annotated[list[SessionRelatedReadWithRelationsForMovie], Field(default_factory=list)]

    model_config = ConfigDict(from_attributes=True)
