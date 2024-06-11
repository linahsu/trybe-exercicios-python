class Product:
    def __init__(self, name: str, price: float) -> None:
        self._name = name
        self._price = price

    def get_description(self) -> str:
        return f"O preço do produto {self._name} é R${self._price}"

    def get_price(self) -> str:
        return f"O preço do produto é R${self._price}"


class Book(Product):
    def __init__(self, name: str, price: float, author: str) -> None:
        super().__init__(name, price)
        self._author = author

    def get_description(self) -> str:
        return f"O preço do livro {self._name}, do autor {self._author} é R${self._price}"  # noqa E501

    def get_price(self) -> str:
        return f"O preço do livro é R${self._price}"


class DVD(Product):
    def __init__(self, name: str, price: float, direction: str) -> None:
        super().__init__(name, price)
        self._direction = direction

    def get_description(self) -> str:
        return f"O preço do DVD {self._name}, da direção {self._direction} é R${self._price}"  # noqa E501

    def get_price(self) -> str:
        return f"O preço do DVD é R${self._price}"


if __name__ == "__main__":
    produto = Product("caneta", 1.99)
    book = Book("Harry Potter", 69.99, "J.K. Rowling")
    dvd = DVD("HITCHCOCK", 39.99, "Sacha Gervasi")

    print(
        "Descrição do produto: ",
        produto.get_description(),
        produto.get_price(),  # noqa E501
    )  # noqa E501
    print("Descrição do livro: ", book.get_description(), book.get_price())
    print("Descrição do dvd: ", dvd.get_description(), dvd.get_price())
