from pydantic import BaseModel, ConfigDict, PositiveInt


class Id(BaseModel):
    id: PositiveInt

    model_config = ConfigDict(from_attributes=True)
