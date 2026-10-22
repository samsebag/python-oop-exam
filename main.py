"""Demo of the Customer's Order Management System and the bonus."""
from order_system import (
    Customer, CustomerType, DuplicateIdError, FlowersGift, Item,
    NotVipCustomerError, PaymentType, RegularOrder, VipOrder,
)
from bonus import Cat, Fish, Spider


def main():
    print("=== Customers ===")
    dana = Customer(1, "Dana", "Cohen", "dana@mail.com", "Tel Aviv",
                    CustomerType.VIP, discount=10)
    yossi = Customer(2, "Yossi", "Levi", "yossi@mail.com", "Haifa")
    print(dana, yossi, sep="\n")

    print("\n=== Items ===")
    laptop = Item(101, "Laptop", 3000)
    mouse = Item(102, "Mouse", 100)
    mouse_2 = Item(103, "mouse", 90)  # same name, different id -> same item
    print(laptop, mouse, mouse_2, sep="\n")

    print("\n=== Regular order (no discount) ===")
    o1 = RegularOrder(1001, "Office setup", "Haifa", [laptop, mouse],
                      yossi, PaymentType.CASH)
    print(o1, "->", o1.total_price)

    print("\n=== VIP order (10% discount) ===")
    o2 = VipOrder(1002, "Dana's order", "Tel Aviv", [laptop, mouse],
                  dana, PaymentType.CREDIT_CARD)
    print(o2, "->", o2.total_price)

    print("\n=== VIP order for a regular customer -> error ===")
    try:
        VipOrder(1003, "Bad order", "Haifa", [mouse], yossi, PaymentType.CHECK)
    except NotVipCustomerError as e:
        print("Error:", e)

    print("\n=== Duplicate order id -> error ===")
    try:
        RegularOrder(1001, "Duplicate", "Haifa", [mouse], yossi, PaymentType.OTHER)
    except DuplicateIdError as e:
        print("Error:", e)

    print("\n=== Favorite items (no duplicates by name) ===")
    RegularOrder(1004, "More mice", "Haifa", [mouse_2], yossi, PaymentType.CASH)
    print([i.name for i in yossi.favorite_items])
    yossi.remove_favorite_item("Laptop")
    yossi.add_favorite_item(Item(104, "Keyboard", 250))
    print([i.name for i in yossi.favorite_items])

    print("\n=== Gifts ===")
    dana.take_gift(FlowersGift())
    dana.open_gift()
    dana.open_gift()  # no gift anymore

    print("\n=== Bonus ===")
    for animal in (Spider(), Cat("Mitzi"), Fish()):
        animal.walk()
        animal.eat()
    fish = Fish()
    fish.set_name("Nemo")
    fish.play()


if __name__ == "__main__":
    main()
