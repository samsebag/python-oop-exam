from abc import ABC, abstractmethod


class Gift(ABC):
    """
    Interface for customer gifts.
    A gift can be of any type, but it must implement open_gift().
    """

    @abstractmethod
    def open_gift(self):
        pass


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
