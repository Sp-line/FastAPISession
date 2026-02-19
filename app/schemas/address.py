from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict, PositiveInt

from constants import AddressLimits
from schemas.base import Id


class AddressBase(BaseModel):
    city: Annotated[str, Field(min_length=AddressLimits.CITY_MIN, max_length=AddressLimits.CITY_MAX)]
    street: Annotated[str, Field(min_length=AddressLimits.STREET_MIN, max_length=AddressLimits.STREET_MAX)]
    house_number: Annotated[
        str, Field(min_length=AddressLimits.HOUSE_NUMBER_MIN, max_length=AddressLimits.HOUSE_NUMBER_MAX)]
    zip_code: Annotated[str, Field(min_length=AddressLimits.ZIP_CODE_MIN, max_length=AddressLimits.ZIP_CODE_MAX)]
    latitude: Annotated[float, Field(ge=AddressLimits.LATITUDE_MIN, le=AddressLimits.LATITUDE_MAX)]
    longitude: Annotated[float, Field(ge=AddressLimits.LONGITUDE_MIN, le=AddressLimits.LONGITUDE_MAX)]


class AddressBaseWithRelations(AddressBase):
    cinema_id: PositiveInt


class AddressCreateDB(AddressBaseWithRelations):
    pass


class AddressCreateReq(AddressBaseWithRelations):
    pass


class AddressUpdateBase(BaseModel):
    city: Annotated[str | None, Field(min_length=AddressLimits.CITY_MIN, max_length=AddressLimits.CITY_MAX)] = None
    street: Annotated[
        str | None, Field(min_length=AddressLimits.STREET_MIN, max_length=AddressLimits.STREET_MAX)] = None
    house_number: Annotated[
        str | None, Field(min_length=AddressLimits.HOUSE_NUMBER_MIN, max_length=AddressLimits.HOUSE_NUMBER_MAX)] = None
    zip_code: Annotated[
        str | None, Field(min_length=AddressLimits.ZIP_CODE_MIN, max_length=AddressLimits.ZIP_CODE_MAX)] = None
    latitude: Annotated[
        float | None, Field(ge=AddressLimits.LATITUDE_MIN, le=AddressLimits.LATITUDE_MAX)] = None
    longitude: Annotated[
        float | None, Field(ge=AddressLimits.LONGITUDE_MIN, le=AddressLimits.LONGITUDE_MAX)] = None


class AddressUpdateDB(AddressUpdateBase):
    cinema_id: PositiveInt | None = None


class AddressUpdateReq(AddressUpdateBase):
    pass


class AddressRead(Id, AddressBase):
    model_config = ConfigDict(from_attributes=True)


class AddressRelatedRead(Id, AddressBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
