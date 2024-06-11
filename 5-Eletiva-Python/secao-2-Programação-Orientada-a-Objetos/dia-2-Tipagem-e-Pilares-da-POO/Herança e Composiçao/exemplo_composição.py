from HomeAppliance import Blender


class Person:
    def __init__(self, name: str, account_balance: float) -> None:
        self.name = name
        self.account_balance = account_balance
        self.blender: Blender | None = None

    def buy_blender(self, blender: Blender) -> None:
        if blender.price <= self.account_balance:
            self.account_balance -= blender.price
            self.blender = blender


person = Person("Jacquin", 1000.0)
red_blender = Blender("red", 1000, 220, 350.0)
person.buy_blender(red_blender)
