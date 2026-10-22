class OrderSystemError(Exception):
    """Base class for all errors raised by the order system."""


class DuplicateIdError(OrderSystemError):
    """Raised when an id that must be unique is used twice."""


class NotVipCustomerError(OrderSystemError):
    """Raised when a VIP order is created for a customer who is not VIP."""


class InvalidValueError(OrderSystemError):
    """Raised when a property receives an invalid value."""
