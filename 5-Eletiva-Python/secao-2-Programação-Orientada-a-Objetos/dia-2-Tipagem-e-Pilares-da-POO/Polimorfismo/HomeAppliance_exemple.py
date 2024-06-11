from typing import List, Union
from HomeAppliance import HomeAppliance


class Blender(HomeAppliance):
    pass


class Fan(HomeAppliance):
    def __init__(
        self,
        color: str,
        power: int,
        voltage: int,
        price: Union[float, int],
        amount_of_fan_speed=1,
    ) -> None:
        # Chamada ao construtor da superclasse
        super().__init__(color, power, voltage, price)

        # Faz outras coisas específicas dessa subclasse
        self.amount_of_fan_speed = amount_of_fan_speed


class Person:
    def __init__(self, name, account_balance: int) -> None:
        self.name = name
        self.account_balance = account_balance
        self.home_appliances: List[HomeAppliance] = []

    # Permite a aquisição de qualquer eletrodoméstico
    def buy_home_appliance(self, home_appliance: HomeAppliance) -> None:
        if home_appliance.price <= self.account_balance:
            self.account_balance -= home_appliance.price
            self.home_appliances.append(home_appliance)
