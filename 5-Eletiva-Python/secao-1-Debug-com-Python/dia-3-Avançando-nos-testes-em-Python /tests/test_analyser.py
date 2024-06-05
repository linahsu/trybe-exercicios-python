# Passo 1
from unittest.mock import Mock, patch

from analyser import analyze_json_file, read_json_file

import pytest


def test_analyze_json_file():
    # Passo 2
    mock_read_json_file = Mock(return_value={"nome": "Maria", "idade": 31})
    fake_file_path = "invalid.json"

    # Passo 3
    # Anota aí 📝: Podemos usar o patch como um decorador (@patch(...)) acima
    # da assinatura da função, ou como um context manager (with patch(...):)
    # dentro da função. Nesse exemplo utilizamos o context manager, e temos a
    # vantagem de que o patch só está aplicado ‘dentro’ da identação do with.
    with patch("analyzer.read_json_file", mock_read_json_file):
        result = analyze_json_file(fake_file_path)

    assert result == "A pessoa de nome Maria tem 31 anos de idade."
    +mock_read_json_file.assert_called_with(fake_file_path)


def test_analyze_json_file_with_mock():
    mock_read_json_file = Mock(
        side_effect=[
            {"nome": "Maria", "idade": 31},
            {"nome": "Agenor", "idade": 86},
        ]
    )
    fake_file_path = "invalid.json"

    with patch("analyzer.read_json_file", mock_read_json_file):
        assert (
            analyze_json_file(fake_file_path)
            == "A pessoa de nome Maria possui 31 anos de idade."
        )
        assert (
            analyze_json_file(fake_file_path)
            == "A pessoa de nome Agenor possui 86 anos de idade."
        )

    mock_read_json_file.assert_called_with(fake_file_path)


def test_analyze_json_file_propagates_exception():
    mock_read_json_file = Mock(side_effect=FileNotFoundError)
    fake_file_path = "invalid.json"

    with patch("analyzer.read_json_file", mock_read_json_file):
        with pytest.raises(FileNotFoundError):
            analyze_json_file(fake_file_path)


def test_read_json_file(tmp_path):
    fake_file_path = tmp_path / "fake.json"
    fake_file_path.touch()

    mock_json = Mock()
    mock_json.load = Mock(return_value={"nome": "Maria", "idade": 31})

    with patch("analyzer.json", mock_json):
        result = read_json_file(fake_file_path)

    assert result == {"nome": "Maria", "idade": 31}


def test_invalid_json_file():
    file_path = "person_data.csv"
    with pytest.raises(
        ValueError, match="O arquivo precisa ser um arquivo JSON."
    ):  # noqa E501
        analyze_json_file(file_path)


# pytest --cov
# python3 -m pytest --cov
# Para entender qual linha não foi executada no arquivo analyzer.py, é
# possível usar o argumento --cov-report=term-missing. Adicionando
# essas duas alterações, o comando fica assim:
# pytest --cov analyzer --cov-report=term-missing

# Anota aí 📝: O argumento --cov recebe um ou mais módulos ou pacotes, por
# isso não se coloca o .py ao final de analyzer. Se for passado apenas o
# nome do pacote (pasta), será calculada a cobertura de todos os arquivos
# do pacote. Já se for passado apenas o nome de um módulo (arquivo), o
# cálculo será apenas daquele módulo.
