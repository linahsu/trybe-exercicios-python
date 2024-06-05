def test_a_simple_test():
    assert True


def test_sum(my_list):  # Recebemos a fixture como parâmetro da função de teste
    assert sum(my_list) == 6  # Usamos a lista retornada pela fixture


# rodando o test junto com o doctest no arquivo main.py
# pytest --doctest-modules -vv
