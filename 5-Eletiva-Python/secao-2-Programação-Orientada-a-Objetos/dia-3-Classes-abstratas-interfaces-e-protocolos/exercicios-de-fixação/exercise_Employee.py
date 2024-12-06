from abc import ABC, abstractmethod


class Employee(ABC):
    def __init__(self, name, salary):
        self.name = name
        self._salary = salary

    @abstractmethod
    def calculate_bonus(self) -> str:
        pass


class Developer(Employee):
    def calculate_bonus(self) -> str:
        """Para o Developer o bônus será de 20% do salário"""
        with_bonus = self._salary * 1.2
        return (
            f"O salário do programador {self.name} mais "
            f"bonificação é de R${format(with_bonus, '.2f')}"
            # f"bonificação é de R${'{:.2f}'.format(with_bonus)}"
        )


class Analyst(Employee):
    def calculate_bonus(self) -> str:
        """Para o Analyst o bônus será de 30% do salário"""
        with_bonus = self._salary * 1.3
        return (
            f"O salário do programador {self.name} mais "
            f"bonificação é de R${format(with_bonus, '.2f')}"
            # f"bonificação é de R${'{:.2f}'.format(with_bonus)}"
        )


class Manager(Employee):
    def calculate_bonus(self) -> str:
        """Para o Manager o bônus será de 40% do salário"""
        with_bonus = self._salary * 1.4
        return (
            f"O salário do programador {self.name} mais "
            f"bonificação é de R${format(with_bonus, '.2f')}"
            # f"bonificação é de R${'{:.2f}'.format(with_bonus)}"
        )


class Worker(Employee):
    def calculate_bonus(self) -> str:
        """Para as demais funções o bônus será de 10% do salário"""
        with_bonus = self._salary * 1.1
        return (
            f"O salário do programador {self.name} mais "
            f"bonificação é de R${format(with_bonus, '.2f')}"
            # f"bonificação é de R${'{:.2f}'.format(with_bonus)}"
        )


def main():
    developer = Developer("Lina", 10000)
    analyst = Analyst("Rebecca", 5000)
    manager = Manager("Luiz", 12000)
    worker = Worker("Andre", 4000)

    print(developer.calculate_bonus())
    print(analyst.calculate_bonus())
    print(manager.calculate_bonus())
    print(worker.calculate_bonus())


if __name__ == "__main__":
    main()
