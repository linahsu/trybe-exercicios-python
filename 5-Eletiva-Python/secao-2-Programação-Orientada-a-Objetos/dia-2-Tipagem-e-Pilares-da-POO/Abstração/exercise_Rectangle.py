class Rectangle:
    def __init__(self, base: int, height: int) -> None:
        self.base = base
        self.height = height

    def calculate_area(self):
        return self.base * self.height

    def calculate_perimeter(self):
        return (self.base * 2) + (self.height * 2)


if __name__ == "__main__":
    rectangle_1 = Rectangle(5, 10)
    print("Área: ", rectangle_1.calculate_area())
    print("Perímetro: ", rectangle_1.calculate_perimeter())
