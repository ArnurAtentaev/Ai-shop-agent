from pydantic import ConfigDict
from .base_schemas import ShopBase, RatingShopBase


class GetShop(ShopBase):
    model_config = ConfigDict(from_attributes=True)


class CreateShop(GetShop):
    pass


class GetRatingShop(RatingShopBase):
    model_config = ConfigDict(from_attributes=True)


class CreateRatingShop(GetRatingShop):
    shop_id: int
