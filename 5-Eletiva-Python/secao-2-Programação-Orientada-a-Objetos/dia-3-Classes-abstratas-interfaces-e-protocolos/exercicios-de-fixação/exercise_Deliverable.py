from abc import ABC, abstractmethod
from faker import Faker

faker = Faker("pt-BR")


class Customer:
    def __init__(self, name: str, phone: int) -> None:
        self.name = name
        self.phone = phone


class Address:
    def __init__(
        self, street: str, number: int, city: str, state: str
    ) -> None:  # noqa E501
        self.street = street
        self.number = number
        self.city = city
        self.state = state


class Delivarable(ABC):
    @abstractmethod
    def delivery(self, customer: Customer, address: Address) -> None:
        pass


class Mail(Delivarable):
    def delivery(self, customer: Customer, address: Address) -> None:
        print(
            f"A correspondência do cliente {customer.name} "
            f"foi entregue no endereço {address.street} com sucesso"
        )


class ShippingCompany(Delivarable):
    def delivery(self, customer: Customer, address: Address) -> None:
        print(
            f"O pacote do cliente {customer.name} "
            f"foi entregue no endereço {address.street} com sucesso"
        )


def main() -> None:
    customer = Customer(faker.name(), faker.phone_number())
    address = Address(
        faker.street_name(), faker.building_number(), faker.city(), "São Paulo"
    )  # noqa E501
    mail = Mail()
    shipping = ShippingCompany()

    mail.delivery(customer, address)
    shipping.delivery(customer, address)


if __name__ == "__main__":
    main()
