class Animal:
    def __init__(self, name: str) -> None:
        self.name = name

    def make_sound(self) -> str:
        print(f"Animal {self.name} fazendo som")


class Mamal(Animal):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def breast_feed(self):
        print(f"Mamal {self.name} is breast feeding")


class Dog(Mamal):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def bark(self):
        print(f"Dog {self.name}: Au au!")


if __name__ == "__main__":
    barney = Dog("Barney")
    barney.make_sound()
    barney.breast_feed()
    barney.bark()
