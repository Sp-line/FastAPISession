from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import CinemaLimits
from schemas.address import AddressRelatedRead
from schemas.base import Id


class CinemaBase(BaseModel):
    name: Annotated[str, Field(min_length=CinemaLimits.NAME_MIN, max_length=CinemaLimits.NAME_MAX)]
    description: str | None = None
    is_available: bool = True


class CinemaCreateDB(CinemaBase):
    slug: Annotated[str, Field(min_length=CinemaLimits.SLUG_MIN, max_length=CinemaLimits.SLUG_MAX)]


class CinemaCreateReq(CinemaBase):
    pass


class CinemaUpdateBase(BaseModel):
    name: Annotated[str | None, Field(min_length=CinemaLimits.NAME_MIN, max_length=CinemaLimits.NAME_MAX)] = None
    description: str | None = None
    is_available: bool | None = None


class CinemaUpdateDB(CinemaUpdateBase):
    slug: Annotated[str | None, Field(min_length=CinemaLimits.SLUG_MIN, max_length=CinemaLimits.SLUG_MAX)] = None


class CinemaUpdateReq(CinemaUpdateBase):
    pass


class CinemaRead(Id, CinemaBase):
    address: AddressRelatedRead

    model_config = ConfigDict(from_attributes=True)
