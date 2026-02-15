from pydantic import ConfigDict

from .base_schemas import InsertOrderBase, OrderItemBase, OrderBase, OrdersBase


class CreateInsertOrder(InsertOrderBase):
    model_config = ConfigDict(from_attributes=True)


class GetOrderItem(OrderItemBase):
    model_config = ConfigDict(from_attributes=True)


class GetOrder(OrderBase):
    model_config = ConfigDict(from_attributes=True)


class GetOrders(OrdersBase):
    model_config = ConfigDict(from_attributes=True)


class CreateOrders(GetOrders):
    pass
