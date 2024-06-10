import pytest


@pytest.fixture(scope="session", autouse=True)
def faker_seed():
    return "Trybe"


# Anota aí 📝: passar para uma fixture autouse=True faz com que ela seja
# utilizada pelas funções de teste mesmo que elas não recebam a fixture
# explicitamente como parâmetro.


@pytest.fixture(scope="session", autouse=True)
def faker_locale():
    return "pt_BR"


# Alguns pontos importantes sobre o exemplo:

# - A fixture faker_seed foi criada no arquivo conftest.py para que possa ser
# usada em todos os testes.
# - A fixture faker_seed foi configurada com o escopo session para que a seed
# seja aplicada em todos os testes.
# - A fixture faker_seed foi configurada com o parâmetro autouse=True para que
# a seed seja aplicada automaticamente em todos os testes.
