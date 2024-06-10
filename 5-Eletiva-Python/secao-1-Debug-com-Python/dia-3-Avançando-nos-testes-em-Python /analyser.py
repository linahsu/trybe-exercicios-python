import json


def read_json_file(file_path):
    with open(file_path, "r") as file:
        return json.load(file)


def analyze_json_file(file_path) -> str:
    if not file_path.endswith(".json"):
        raise ValueError("O arquivo precisa ser um arquivo JSON.")

    data = read_json_file(file_path)
    return (
        f"A pessoa de nome {data['nome']} "
        f"tem {data['idade']} anos de idade."  # noqa E501
    )  # noqa E501
