from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from .customer import Customer
from .enums import PaymentType
from .exceptions import DuplicateIdError, InvalidValueError, NotVipCustomerError
from .item import Item
from .unique_id import UniqueIdMixin


class Order(UniqueIdMixin, ABC):
    """
    Abstract order. RegularOrder and VipOrder share the same id registry,
    so an order id is unique across both order types.
    """

    _used_ids = set()

    def __init__(
        self,
        order_id,
        name: str,
        delivery_address: str,
        items: List[Item],
        customer: Customer,
        payment_type: PaymentType,
        order_date: Optional[datetime] = None,
    ):
        self._validate(order_id, items, customer, payment_type)
        self.name = name
        self.delivery_address = delivery_address
        self.__items = list(items)
        self.__customer = customer
        self.payment_type = payment_type
        self.__order_date = order_date or datetime.now()

        # Required by the spec: the constructor calculates the total price.
        # (For a VIP order this raises NotVipCustomerError if the customer is not VIP.)
        self.__total_price = self.calculate_total_price()

        # The id is reserved only once the order is valid, so a rejected
        # order does not "burn" its id.
        self.__id = self._register_id(order_id)

        # Required by the spec: order items are added to the customer's favorites
        customer.add_favorite_items(self.__items)

    def _validate(self, order_id, items, customer, payment_type):
        if order_id in self._used_ids:
            raise DuplicateIdError(f"Order id {order_id!r} already exists")
        if not isinstance(customer, Customer):
            raise InvalidValueError("customer must be a Customer")
        if not isinstance(payment_type, PaymentType):
            raise InvalidValueError("payment_type must be a PaymentType")
        if not isinstance(items, (list, tuple)) or not all(isinstance(i, Item) for i in items):
            raise InvalidValueError("items must be a list of Item objects")
        ids = [item.id for item in items]
        if len(ids) != len(set(ids)):
            raise DuplicateIdError("An order cannot contain two items with the same id")

    # ---------- properties ----------
    @property
    def id(self):
        return self.__id

    @property
    def items(self) -> List[Item]:
        return list(self.__items)

    @property
    def customer(self) -> Customer:
        return self.__customer

    @property
    def total_price(self) -> float:
        return self.__total_price

    @property
    def order_date(self) -> datetime:
        return self.__order_date

    def _items_sum(self) -> float:
        return sum(item.price for item in self.__items)

    @abstractmethod
    def calculate_total_price(self) -> float:
        pass

    def __repr__(self):
        return (
            f"{type(self).__name__}(id={self.id!r}, customer={self.customer.id!r}, "
            f"total={self.total_price}, payment={self.payment_type.value})"
        )


class RegularOrder(Order):
    def calculate_total_price(self) -> float:
        # Regular orders: no discount
        return round(self._items_sum(), 2)


class VipOrder(Order):
    def calculate_total_price(self) -> float:
        # Check the customer is VIP before calculating
        if not self.customer.is_vip():
            raise NotVipCustomerError(
                f"Customer {self.customer.id!r} is not a VIP customer "
                f"and cannot make a VIP order"
            )
        discount = self.customer.discount or 0  # discount can be None
        return round(self._items_sum() * (1 - discount / 100), 2)
