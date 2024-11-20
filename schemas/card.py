
from pydantic import computed_field, BaseModel,Field


class CardCreate(BaseModel):
    quantity:int = Field(gt=0)
    period:int = Field(gt=0)