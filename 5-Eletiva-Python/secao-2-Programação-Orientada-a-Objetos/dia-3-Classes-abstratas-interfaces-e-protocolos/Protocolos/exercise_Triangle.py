from exercise_CalculatePerimeter import CalculatePerimeter


class Triangle(CalculatePerimeter):
    def __init__(self, side_1: int, side_2: int, side_3: int) -> None:
        self.side_1 = side_1
        self.side_2 = side_2
        self.side_3 = side_3

    def calculate_area(self) -> str:
        return f"O perímetro do triângulo é de {self.side_1 + self.side_2 + self.side_3} cm"  # noqa E501

    def calculate_perimeter(self) -> str:
        perimeter = self.side_1 + self.side_2 + self.side_3
        return f"O perímetro do triângulo é {perimeter}"


triangle = Triangle(5, 5, 5)
print(triangle.calculate_area())
