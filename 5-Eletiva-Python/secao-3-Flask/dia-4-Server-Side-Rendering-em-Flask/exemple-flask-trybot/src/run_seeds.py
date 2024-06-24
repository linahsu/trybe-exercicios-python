from models.joke_model import JokeModel

jokes = [
    "Porque a galinha atravessou a rua? Para chegar do outro lado",
    "Qual o contrário de volátil? Vem cá sobrinho",
    "O que é um pontinho amarelo no céu? Um Yellowcóptero",
    "O que é um pontinho verde no canto da sala? Uma ervilha fazendo exercício",
    "O que é um pontinho azul no canto da sala? Um smurfs fazendo exercício"
]

for joke in jokes:
    JokeModel({'joke': joke}).save()

# python3 -m venv .venv && source .venv/bin/activate
# pip install --no-cache-dir -r src/dev-requirements.txt
# python3 src/run_seeds.py