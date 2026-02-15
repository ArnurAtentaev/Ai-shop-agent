from pydantic import BaseModel, ConfigDict, Field


class ShopBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    city: str


class RatingShopBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    scores: int = Field(ge=1, le=5, default=1)
