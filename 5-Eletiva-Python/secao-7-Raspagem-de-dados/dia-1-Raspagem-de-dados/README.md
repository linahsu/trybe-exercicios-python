# Raspagem de dados

<details>
<summary><strong> Instalação do módulo request </strong></summary>

### Requisições web

A comunicação com servidores HTTP e HTTPS se dá através de requisições, nas quais utilizamos o verbo para indicar que tipo de ação deve ser tomada para um dado recurso. Devemos informar na requisição em qual recurso estamos atuando e no cabeçalho passamos algumas informações que podem ser importantes, como o tipo de resposta aceita ou o tipo de conteúdo sendo enviado.

O Python possui um pacote para lidar com o protocolo HTTP o urllib, porém seu uso é mais verboso. Por isso vamos utilizar a biblioteca requests, que possui uma interface mais amigável e é bem difundida na comunidade.

Você já pode instalar a requests dentro de um ambiente virtual, com os seguintes comandos:

```bash
python3 -m venv .venv && source .venv/bin/activate
python3 -m pip install requests
```

Abaixo vamos ver alguns exemplos de como utilizar a biblioteca requests:

```bash
import requests


# Requisição do tipo GET
response = requests.get("https://www.betrybe.com/")
print(response.status_code)  # código de status
print(response.headers["Content-Type"])  # conteúdo no formato html

# Conteúdo recebido da requisição
print(response.text)

# Bytes recebidos como resposta
print(response.content)

# Requisição do tipo post
response = requests.post("http://httpbin.org/post", data="some content")
print(response.text)

# Requisição enviando cabeçalho (header)
response = requests.get("http://httpbin.org/get", headers={"Accept": "application/json"})
print(response.text)

# Requisição a recurso binário
response = requests.get("http://httpbin.org/image/png")
print(response.content)

# Recurso JSON
response = requests.get("http://httpbin.org/get")
# Equivalente ao json.loads(response.content)
print(response.json())

# Podemos também pedir que a resposta lance uma exceção caso o status não seja OK
response = requests.get("http://httpbin.org/status/404")
response.raise_for_status()
```

```bash
```

</details>
</br>

<details>
<summary><strong>  </strong></summary>


```bash
```

```bash
```

```bash
```

</details>
</br>

<details>
<summary><strong>  </strong></summary>


```bash
```

```bash
```

```bash
```

</details>
</br>