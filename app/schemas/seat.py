from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict

from constants import SeatLimits, SeatType
from schemas.base import Id


class SeatBase(BaseModel):
    is_active: bool = True
    type: SeatType

    row_label: Annotated[str, Field(min_length=SeatLimits.ROW_LABEL_MIN, max_length=SeatLimits.ROW_LABEL_MAX)]
    column_label: Annotated[str, Field(min_length=SeatLimits.COLUMN_MIN, max_length=SeatLimits.COLUMN_LABEL_MAX)]

    row: Annotated[int, Field(ge=SeatLimits.ROW_MIN)]
    column: Annotated[int, Field(ge=SeatLimits.COLUMN_MIN)]


class SeatBaseWithRelations(SeatBase):
    hall_id: Annotated[int, Field(ge=1)]


class SeatCreateDB(SeatBaseWithRelations):
    pass


class SeatCreateReq(SeatBaseWithRelations):
    pass


class SeatUpdateBase(BaseModel):
    is_active: bool | None = None
    type: SeatType | None = None

    row_label: Annotated[
        str | None, Field(min_length=SeatLimits.ROW_LABEL_MIN, max_length=SeatLimits.ROW_LABEL_MAX)] = None
    column_label: Annotated[
        str | None, Field(min_length=SeatLimits.COLUMN_LABEL_MIN, max_length=SeatLimits.COLUMN_LABEL_MAX)] = None

    row: Annotated[int | None, Field(ge=SeatLimits.ROW_MIN)] = None
    column: Annotated[int | None, Field(ge=SeatLimits.COLUMN_MIN)] = None


class SeatUpdateDB(SeatUpdateBase):
    hall_id: Annotated[int | None, Field(ge=1)] = None


class SeatUpdateReq(SeatUpdateBase):
    pass


class SeatRead(Id, SeatBaseWithRelations):
    model_config = ConfigDict(from_attributes=True)
