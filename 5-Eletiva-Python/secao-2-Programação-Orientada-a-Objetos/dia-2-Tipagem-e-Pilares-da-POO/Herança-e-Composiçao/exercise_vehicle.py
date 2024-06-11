class Vehicle:
    def __init__(self, name: str, capacity: int) -> None:
        self.name = name
        self.capacity = capacity

    def move(self, distance: int) -> str:
        return f"{self.name} carried {self.capacity} people across {distance} kilometers."  # noqa E501


class Car(Vehicle):
    def __init__(self, capacity) -> None:
        super().__init__("Car", capacity)


class Motorcycle(Vehicle):
    def __init__(self) -> None:
        super().__init__("Motorcycle", 2)


if __name__ == "__main__":
    car = Car(4)
    print(car.move(200))
    motorcycle = Motorcycle()
    print(motorcycle.move(10))
