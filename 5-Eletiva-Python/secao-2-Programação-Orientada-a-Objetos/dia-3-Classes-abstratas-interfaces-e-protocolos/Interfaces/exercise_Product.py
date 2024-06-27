from abc import ABC, abstractmethod


class Product(ABC):
    @abstractmethod
    def print_price(self) -> None:
        raise NotImplementedError(
            "O método para imprimir o preço deve ser implementado"
        )


class Book(Product):
    def __init__(self, price: float) -> None:
        self._price = price

    def print_price(self) -> None:
        print(f"O preço do livro é R${self._price}")


if __name__ == "__main__":
    livro = Book(29.99)
    livro.print_price()
