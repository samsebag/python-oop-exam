from .exceptions import DuplicateIdError


class UniqueIdMixin:
    """
    Enforces unique ids. Each class that uses it defines its own
    `_used_ids` set (Item, Customer, Order). Subclasses such as
    RegularOrder and VipOrder inherit their parent's set, so an order id
    is unique across both order types.
    """

    _used_ids: set

    def _register_id(self, obj_id):
        if obj_id is None:
            raise DuplicateIdError("An id is required")
        if obj_id in self._used_ids:
            raise DuplicateIdError(
                f"{type(self).__name__} id {obj_id!r} already exists"
            )
        self._used_ids.add(obj_id)
        return obj_id

    @classmethod
    def _reset_ids(cls):
        """Clear the registry (used by the tests)."""
        cls._used_ids.clear()
