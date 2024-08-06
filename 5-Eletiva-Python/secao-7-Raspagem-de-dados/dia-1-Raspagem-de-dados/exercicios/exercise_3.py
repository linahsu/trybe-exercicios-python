# Exercicio 3: Às vezes, você precisa fazer com que o seu raspador da Web
# pareça estar fazendo solicitações HTTP como o navegador, para que o
# servidor retorne os mesmos dados que você vê no seu navegador. Faça uma
# requisição a https://scrapethissite.com/pages/advanced/?gotcha=headers e
# verifique se foi bem sucedida.
# ⚠️ Para verificar se a requisição foi bem sucedida, faça (assert "User-Agent
# value doesn't look like a standard mozilla/chrome/safari value" not in
# response.text). Se nada acontecer, seu código está funcionando. ⚠️ Faça a
# inspeção de como a requisição é feita pelo navegador para conseguir replicar
# através do código.

import requests

response = requests.get(
    "https://scrapethissite.com/pages/advanced/?gotcha=headers",
    headers={'User-Agent': 'Mozilla', "Accept": "text/html"}
)
assert (
    "User-Agent value doesn't look like a standard mozilla/chrome/safari value"
    not in response.text
)
