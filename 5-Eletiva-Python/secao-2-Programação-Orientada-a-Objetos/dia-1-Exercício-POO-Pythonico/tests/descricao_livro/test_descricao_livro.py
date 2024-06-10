import pytest
from src.livro.livro import Livro


@pytest.fixture
def livro():
    return Livro("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 235)


def test_descricao_livro(livro):
    assert livro.__repr__() == (
        "O livro Harry Potter e a Pedra Filosofal"
        " de J.K. Rowling"
        " possui 235 páginas."
    )
