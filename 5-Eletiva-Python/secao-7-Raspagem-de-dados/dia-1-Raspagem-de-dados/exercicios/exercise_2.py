import requests


# Exercicio 2: Faça uma requisição ao recurso usuários da API do Github
# (https://api.github.com/users), exibindo o username e url de todos os
# usuários retornados.

response = requests.get("https://api.github.com/users")
users = response.json()

for user in users:
    print(f"{user['login']} {user['url']}")
