from abc import ABC, abstractmethod


class Person(ABC):
    @abstractmethod
    def print_role(self):
        pass


class Seller(Person):
    def print_role(self):
        print("Meu cargo é de vendedor")


class Manager(Person):
    def print_role(self):
        print("Meu cargo é de gerente")


if __name__ == "__main__":
    vendedor = Seller()
    gerente = Manager()

    print(vendedor.print_role())
    print(gerente.print_role())
