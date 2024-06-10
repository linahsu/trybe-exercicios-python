import pytest
from src.livro.livro import Livro


@pytest.fixture
def livro():
    return Livro("Harry Potter e a Pedra Filosofal", "J.K. Rowling", 235)


def test_cria_livro(livro):
    assert livro.titulo == "Harry Potter e a Pedra Filosofal"
    assert livro.autor == "J.K. Rowling"
    assert livro.paginas == 235
