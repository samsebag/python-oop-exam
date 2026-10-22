from typing import List, Optional

from .enums import CustomerType
from .exceptions import InvalidValueError
from .gift import Gift
from .item import Item
from .unique_id import UniqueIdMixin


class Customer(UniqueIdMixin):
    """A customer of the website."""

    _used_ids = set()

    def __init__(
        self,
        customer_id,
        first_name: str,
        last_name: str,
        email: str,
        delivery_address: str,
        customer_type: CustomerType = CustomerType.REGULAR,
        discount: Optional[float] = None,
    ):
        self.__id = self._register_id(customer_id)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.delivery_address = delivery_address
        self.customer_type = customer_type
        self.discount = discount
        self.__favorite_items: List[Item] = []
        self.__gift: Optional[Gift] = None

    # ---------- properties ----------
    @property
    def id(self):
        return self.__id

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str):
        if not isinstance(value, str) or "@" not in value:
            raise InvalidValueError("Invalid email address")
        self.__email = value

    @property
    def customer_type(self) -> CustomerType:
        return self.__customer_type

    @customer_type.setter
    def customer_type(self, value: CustomerType):
        if not isinstance(value, CustomerType):
            raise InvalidValueError("customer_type must be a CustomerType")
        self.__customer_type = value

    @property
    def discount(self) -> Optional[float]:
        """Fixed discount rate between 0 and 1 (e.g. 0.05 = 5%). Can be None."""
        return self.__discount

    @discount.setter
    def discount(self, value: Optional[float]):
        if value is not None and (
            not isinstance(value, (int, float)) or not 0 <= value <= 1
        ):
            raise InvalidValueError("Discount must be None or a number between 0 and 1 (e.g. 0.05 = 5%)")
        self.__discount = value

    @property
    def favorite_items(self) -> List[Item]:
        # Return a copy so the list can only be changed through the methods below
        return list(self.__favorite_items)

    @property
    def gift(self) -> Optional[Gift]:
        return self.__gift

    def is_vip(self) -> bool:
        return self.customer_type == CustomerType.VIP

    # ---------- favorite items ----------
    def has_favorite(self, item_name: str) -> bool:
        """Items with the same name (even with a different id) are the same item."""
        return any(
            fav.name.lower() == item_name.strip().lower()
            for fav in self.__favorite_items
        )

    def add_favorite_item(self, item: Item) -> bool:
        if not isinstance(item, Item):
            raise InvalidValueError("Only Item objects can be added to favorites")
        if self.has_favorite(item.name):
            return False
        self.__favorite_items.append(item)
        return True

    def add_favorite_items(self, items: List[Item]):
        for item in items:
            self.add_favorite_item(item)

    def remove_favorite_item(self, item_name: str) -> bool:
        for fav in self.__favorite_items:
            if fav.name.lower() == item_name.strip().lower():
                self.__favorite_items.remove(fav)
                return True
        return False

    # ---------- gifts ----------
    def take_gift(self, gift: Gift):
        if not isinstance(gift, Gift):
            raise InvalidValueError("A gift must implement the Gift interface (open_gift)")
        self.__gift = gift

    def open_gift(self) -> bool:
        """Open the gift if the customer has one. Returns True if a gift was opened."""
        if self.__gift is None:
            print(f"{self.first_name} has no gift to open.")
            return False
        self.__gift.open_gift()
        self.__gift = None
        return True

    def __repr__(self):
        return (
            f"Customer(id={self.id!r}, name='{self.first_name} {self.last_name}', "
            f"type={self.customer_type.value})"
        )
