from typing import Dict


class Estoque:
    def __init__(self, produtos: Dict[str, int]) -> None:
        self.produtos = produtos

    def adicionar_produto_no_estoque(self, nome: str, quantidade: int) -> None:
        if nome in self.produtos:
            self.produtos[nome] += quantidade
        else:
            self.produtos[nome] = quantidade

    def remover_produto_do_estoque(self, nome: str, quantidade: int) -> None:
        if quantidade <= self.produtos[nome]:
            self.produtos[nome] -= quantidade
        else:
            raise ValueError("Quantidade maior do que a quantidade do produto")

    def atualizar_produto_no_estoque(
        self, nome: str, nova_quantidade: int
    ) -> None:
        try:
            if self.produtos[nome]:
                self.produtos[nome] = nova_quantidade
        except KeyError:
            raise ValueError("Produto inexistente no estoque")

    def visualizar_estoque(self) -> None:
        for produto, quantidade in self.produtos.items():
            print(f"{produto}: {quantidade}")
