class MonthlyExpense:
    def __init__(
        self,
        internet: float,
        grocery: float,
        power: float,
        water: float,
        rent: float,  # noqa E501
    ) -> None:
        self.internet = internet
        self.grocery = grocery
        self._power = power
        self._water = water
        self.__rent = rent

    @property
    def power(self) -> float:
        return self._power

    @power.setter
    def power(self, new_power) -> None:
        self._power = new_power

    @property
    def water(self) -> float:
        return self._water

    @water.setter
    def water(self, new_water) -> None:
        self._water = new_water
