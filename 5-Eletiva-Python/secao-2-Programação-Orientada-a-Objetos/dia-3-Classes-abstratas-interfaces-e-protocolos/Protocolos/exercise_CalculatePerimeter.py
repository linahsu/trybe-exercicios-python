from typing import Protocol


class CalculatePerimeter(Protocol):
    def calculate_perimeter(self) -> str:
        pass


class Square(CalculatePerimeter):
    def __init__(self, side):
        self.side = side

    def calculate_perimeter(self) -> str:
        perimeter = self.side * 4
        return f"O perímetro do quadrado é {perimeter}"


if __name__ == "__main__":
    square = Square(4)
    print(square.calculate_perimeter())
