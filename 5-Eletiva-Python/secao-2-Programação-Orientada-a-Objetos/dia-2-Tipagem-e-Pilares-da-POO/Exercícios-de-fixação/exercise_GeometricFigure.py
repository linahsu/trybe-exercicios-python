from typing import Union


class GeometricFigure:
    def area(self) -> Union[int, float]:
        pass

    def perimeter(self) -> Union[int, float]:
        pass


class Square(GeometricFigure):
    def __init__(self, side: int) -> None:
        self.side = side

    def area(self) -> Union[int, float]:
        return self.side**2

    def perimeter(self) -> Union[int, float]:
        return self.side * 4


class Rectangle(GeometricFigure):
    def __init__(self, base: int, height: int) -> None:
        self.base = base
        self.height = height

    def area(self) -> int:
        return self.base * self.height

    def perimeter(self) -> int:
        return (self.base * 2) + (self.height * 2)


class Circle(GeometricFigure):
    def __init__(self, radius: int) -> None:
        self.radius = radius

    def area(self) -> Union[int, float]:
        return 3.14 * (self.radius**2)

    def perimeter(self) -> Union[int, float]:
        return 2 * 3.14 * self.radius


if __name__ == "__main__":
    square = Square(2)
    rectangle = Rectangle(2, 4)
    circle = Circle(2)

    print("Área do quadrado: ", square.area())
    print("Peímetro do quadrado: ", square.perimeter())
    print("Área do retângulo: ", rectangle.area())
    print("Peímetro do retângulo: ", rectangle.perimeter())
    print("Área do círculo: ", circle.area())
    print("Peímetro do círculo: ", circle.perimeter())
