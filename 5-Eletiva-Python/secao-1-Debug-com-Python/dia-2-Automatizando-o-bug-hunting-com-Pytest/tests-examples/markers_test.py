import time

import pytest


@pytest.mark.slow
def test_slow_marker():
    time.sleep(4)


# Você pode executar o comando pytest -m MARKEXPR, no qual MARKEXPR é uma
# expressão que adiciona ou remove a seleção de um ou mais marcadores. Por
# exemplo, ao rodar pytest -m 'not slow' -vv são executados todos os testes,
# menos os marcados como slow.

# É interessante observar que temos um warning, pois criamos um marcador e não
# informamos ao Pytest que ele existe. Para corrigir isso, você pode adicionar
# o seguinte código ao arquivo conftest.py:

# def pytest_configure(config):
#     config.addinivalue_line(
#         "markers", "slow: marks tests as slow"
#     )
