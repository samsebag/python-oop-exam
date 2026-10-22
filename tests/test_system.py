import io
import unittest
from contextlib import redirect_stdout

from order_system import (
    ChocolateBox, Customer, CustomerType, DuplicateIdError, Gift, GiftCard,
    InvalidValueError, Item, NotVipCustomerError, Order, PaymentType,
    RegularOrder, VipOrder,
)
from bonus import Animal, Cat, Fish, Pet, Spider


class BaseTest(unittest.TestCase):
    def setUp(self):
        Item._reset_ids()
        Customer._reset_ids()
        Order._reset_ids()
        self.vip = Customer(1, "Dana", "Cohen", "d@m.com", "TLV", CustomerType.VIP, 0.2)
        self.reg = Customer(2, "Yossi", "Levi", "y@m.com", "Haifa")
        self.a = Item(1, "Book", 50)
        self.b = Item(2, "Pen", 10)


class TestUniqueIds(BaseTest):
    def test_item_id_unique(self):
        with self.assertRaises(DuplicateIdError):
            Item(1, "Other", 5)

    def test_customer_id_unique(self):
        with self.assertRaises(DuplicateIdError):
            Customer(1, "X", "Y", "x@y.com", "addr")

    def test_order_id_unique_across_types(self):
        RegularOrder(10, "o", "addr", [self.a], self.reg, PaymentType.CASH)
        with self.assertRaises(DuplicateIdError):
            VipOrder(10, "o", "addr", [self.a], self.vip, PaymentType.CASH)

    def test_same_item_twice_in_order(self):
        with self.assertRaises(DuplicateIdError):
            RegularOrder(11, "o", "addr", [self.a, self.a], self.reg, PaymentType.CASH)


class TestTotalPrice(BaseTest):
    def test_regular_no_discount(self):
        o = RegularOrder(1, "o", "addr", [self.a, self.b], self.vip, PaymentType.CASH)
        self.assertEqual(o.total_price, 60)

    def test_vip_discount(self):
        o = VipOrder(1, "o", "addr", [self.a, self.b], self.vip, PaymentType.CREDIT_CARD)
        self.assertEqual(o.total_price, 48)

    def test_vip_with_null_discount(self):
        c = Customer(3, "A", "B", "a@b.com", "addr", CustomerType.VIP, None)
        o = VipOrder(1, "o", "addr", [self.a], c, PaymentType.CHECK)
        self.assertEqual(o.total_price, 50)

    def test_vip_order_for_regular_customer_raises(self):
        with self.assertRaises(NotVipCustomerError):
            VipOrder(1, "o", "addr", [self.a], self.reg, PaymentType.CASH)
        # rejected order must not consume the id
        RegularOrder(1, "o", "addr", [self.a], self.reg, PaymentType.CASH)

    def test_order_is_abstract(self):
        with self.assertRaises(TypeError):
            Order(1, "o", "addr", [self.a], self.reg, PaymentType.CASH)

    def test_invalid_payment_type(self):
        with self.assertRaises(InvalidValueError):
            RegularOrder(1, "o", "addr", [self.a], self.reg, "CASH")


class TestFavorites(BaseTest):
    def test_order_adds_favorites_without_duplicates(self):
        RegularOrder(1, "o", "addr", [self.a, self.b], self.reg, PaymentType.CASH)
        same_name = Item(3, "book", 45)  # same name, other id
        RegularOrder(2, "o", "addr", [same_name], self.reg, PaymentType.CASH)
        self.assertEqual([i.name for i in self.reg.favorite_items], ["Book", "Pen"])

    def test_add_and_remove(self):
        self.assertTrue(self.reg.add_favorite_item(self.a))
        self.assertFalse(self.reg.add_favorite_item(self.a))
        self.assertTrue(self.reg.remove_favorite_item("Book"))
        self.assertFalse(self.reg.remove_favorite_item("Book"))
        self.assertEqual(self.reg.favorite_items, [])

    def test_favorites_list_is_protected(self):
        self.reg.favorite_items.append(self.a)
        self.assertEqual(self.reg.favorite_items, [])


class TestGifts(BaseTest):
    def test_open_gift_prints_message(self):
        self.reg.take_gift(GiftCard(100))
        out = io.StringIO()
        with redirect_stdout(out):
            self.assertTrue(self.reg.open_gift())
        self.assertEqual(out.getvalue().strip(),
                         "Congratulations! you got a new gift! Enjoy!")
        self.assertIsNone(self.reg.gift)

    def test_open_without_gift(self):
        with redirect_stdout(io.StringIO()):
            self.assertFalse(self.reg.open_gift())

    def test_any_gift_type_with_open_gift(self):
        class CustomGift(Gift):
            def open_gift(self):
                print("custom")
        self.reg.take_gift(CustomGift())
        self.reg.take_gift(ChocolateBox())

    def test_gift_without_open_gift_rejected(self):
        with self.assertRaises(InvalidValueError):
            self.reg.take_gift("not a gift")


class TestBonus(unittest.TestCase):
    def test_hierarchy(self):
        self.assertTrue(issubclass(Spider, Animal))
        self.assertFalse(issubclass(Spider, Pet))
        for cls in (Cat, Fish):
            self.assertTrue(issubclass(cls, Animal))
            self.assertTrue(issubclass(cls, Pet))

    def test_abstract(self):
        with self.assertRaises(TypeError):
            Animal(4)
        with self.assertRaises(TypeError):
            Pet()

    def test_legs_and_names(self):
        self.assertEqual(Spider()._legs, 8)
        self.assertEqual(Cat()._legs, 4)
        self.assertEqual(Fish()._legs, 0)
        c = Cat("Mitzi")
        self.assertEqual(c.get_name(), "Mitzi")
        c.set_name("Tom")
        self.assertEqual(c.get_name(), "Tom")


if __name__ == "__main__":
    unittest.main()
