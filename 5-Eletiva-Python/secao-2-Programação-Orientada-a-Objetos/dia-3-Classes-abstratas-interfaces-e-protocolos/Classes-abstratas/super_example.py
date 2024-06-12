from abc import ABC, abstractmethod


class X(ABC):
    @abstractmethod
    def example(self) -> None:
        print("Classe-base abstrata")


class Y(X):
    def example(self) -> None:
        super().example()
        print("Subclasse")


z = Y()
z.example()
