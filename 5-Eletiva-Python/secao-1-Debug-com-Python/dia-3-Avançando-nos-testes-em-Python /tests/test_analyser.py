# Passo 1
from unittest.mock import Mock, patch

from analyser import analyze_json_file


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
