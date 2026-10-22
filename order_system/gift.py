from typing import Protocol, runtime_checkable


@runtime_checkable
class Gift(Protocol):
    """
    Interface for customer gifts.
    A gift can be of ANY type, as long as it has an open_gift() method
    (duck typing - no inheritance required).
    """

    def open_gift(self) -> None:
        ...


class BaseGift(Gift):
    """Default behaviour shared by the concrete gifts."""

    MESSAGE = "Congratulations! you got a new gift! Enjoy!"

    def open_gift(self):
        print(self.MESSAGE)


class GiftCard(BaseGift):
    def __init__(self, amount: float):
        self.amount = amount


class FlowersGift(BaseGift):
    def __init__(self, flower_type: str = "roses"):
        self.flower_type = flower_type


class ChocolateBox(BaseGift):
    def __init__(self, pieces: int = 12):
        self.pieces = pieces
