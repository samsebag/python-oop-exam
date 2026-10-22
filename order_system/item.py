from .exceptions import InvalidValueError
from .unique_id import UniqueIdMixin


class Item(UniqueIdMixin):
    """An item that can be part of an order."""

    _used_ids = set()

    def __init__(self, item_id, name: str, price: float):
        self.__id = self._register_id(item_id)
        self.name = name
        self.price = price

    @property
    def id(self):
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise InvalidValueError("Item name must be a non-empty string")
        self.__name = value.strip()

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value < 0:
            raise InvalidValueError("Item price must be a non-negative number")
        self.__price = value

    def __repr__(self):
        return f"Item(id={self.id!r}, name={self.name!r}, price={self.price})"
