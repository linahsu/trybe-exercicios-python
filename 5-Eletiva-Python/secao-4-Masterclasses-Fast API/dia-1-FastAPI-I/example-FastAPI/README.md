# Getting started

Antes de começar a criar código com o FastAPI, precisamos instalá-lo em nosso ambiente virtual! Com o pip, o comando é:

```bash
pip install fastapi
```

Para subir a aplicação localmente, vamos usar o uvicorn: um servidor ASGI (a versão assíncrona do WSGI). Também precisamos instalá-lo:

```bash
pip install uvicorn
```

Feito isso, podemos usar o seguinte comando:

```bash
python3 -m uvicorn main:app
```

### Documentação automática

O FastAPI possui uma funcionalidade muito interessante: a documentação automática. Com ela, podemos acessar a documentação de nossa API em uma página HTML, e até mesmo testar as rotas por lá!

Para acessar a documentação, basta acessar a rota /docs ou /redoc (a diferença é apenas o layout da página). Por exemplo, se estivermos rodando a aplicação localmente, podemos acessar a documentação em http://127.0.0.1:8000/docs.

A documentação automática é gerada a partir do próprio código Python que escrevemos: nomes de funções, nomes de parâmetros, anotações de tipos, docstrings, etc. Por isso, é importante que nosso código esteja bem documentado!

### Criando rotas mais complexas

Em uma API Web podemos ter rotas que fazem uso do body da requisição, parâmetros de query, cabeçalho da requisição, etc. O FastAPI fornece formas de acessar e manipular todos esses itens! As principais páginas de referência na documentação são:

* Parâmetros de rota (path parameters)
* Parâmetros de query (query parameters)
* Corpo da requisição (request body)
* Parâmetros de cabeçalho (header parameters)

### FastAPI e MongoDB

Como o FastAPI é um framework para criação de APIs, ele não possui um ORM (Object Relational Mapper). Por isso, para trabalharmos com bancos de dados, precisamos usar bibliotecas externas.

Já sabemos trabalhar com o Pymongo, mas como o FastAPI é assíncrono, também podemos usar uma biblioteca que seja assíncrona, como Motor.

Para simplificar as aulas, vamos continuar usando o Pymongo

### Modelos com Pydantic

O FastAPI pode utilizar o Pydantic para validação de dados em suas rotas. Isso acontece quando criamos um parâmetro simples, como uma query param que deveria ser int, ou um parâmetro mais complexo, como um body que deveria seguir um modelo.

Para definir esses modelos, usamos a classe BaseModel do Pydantic. A documentação do FastAPI possui uma seção dedicada a isso.

Um modelo simples pode ser definido e utilizado assim:

```bash
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class User(BaseModel):
    name: str
    age: int

@app.post("/users")
def create_user(user: User):
    return user
```

Dessa forma, o FastAPI vai validar se o corpo da requisição segue o modelo definido. Se não seguir, a requisição será rejeitada. Com o exemplo anterior, se enviarmos uma requisição com o corpo:

```bash
{
    "name": "Alguém",
    "age": "idoso"
}
```

O retorno será:

```bash
{
  "detail": [
    {
      "type": "int_parsing",
      "loc": [
        "body",
        "age"
      ],
      "msg": "Input should be a valid integer, unable to parse string as an integer",
      "input": "idoso",
      "url": "https://errors.pydantic.dev/2.5/v/int_parsing"
    }
  ]
}
```

### Configurações com Pydantic Settings

A biblioteca Pydantic, além de prover muitas ferramentas para validações de dados, também pode ser usada para gerenciar configurações de uma aplicação. Ela facilitará o processo de acesso a variáveis de ambiente, além de outros valores globais importantes.

A partir da versão 2 do Pydantic, precisaremos instalar uma extensão para acessar essa funcionalidade especial:

```bash
pip install pydantic-settings
```

Agora, basta criar uma classe que herde de pydantic_settings.BaseSettings e definir os atributos que serão usados como configurações. Por exemplo:

```bash
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )

    app_name: str = "My App"
    minute_rate_limit: int = 100
    mongo_uri: str
```

Nesse caso, utilizamos o atributo especial model_config para indicar que faremos a leitura de um arquivo .env para definir as configurações. Assim, o valor de mongo_uri (que não possui um valor padrão) precisa ser definido no arquivo .env:

```bash
MONGO_URI=mongodb://localhost:27017
```

Sim, a conversão de MONGO_URI para mongo_uri é feita automaticamente! 🤩

Para mais detalhes e exemplos, você pode consultar a documentação do Pydantic Settings ou a página do FastAPI sobre o assunto.

### Rate-limit com slowapi

Conforme nossa aplicação cresce, precisamos ter cada vez mais atenção com sua segurança e performance. Uma das formas de garantir que a API não seja sobrecarregada é limitar o número de requisições que ela pode receber em um determinado período de tempo. Essa limitação é chamada de rate-limit.

O FastAPI não possui uma ferramenta nativa para aplicar rate-limit, mas podemos usar a biblioteca slowapi para isso.

### Middlewares e dependências

O FastAPI permite que criemos middlewares e dependências personalizadas para nossa aplicação. Essas ferramentas são muito úteis para adicionar funcionalidades compartilhadas entre rotas da nossa API, como autenticação, por exemplo.

#### Middlewares

Um middleware é uma função que poderá ser executada antes e depois de cada requisição. Ela pode ser usada para adicionar informações ao contexto da requisição, ou recusar requisições quem possuem (ou não) alguma característica. No FastAPI podemos criar middlewares usando o decorador app.middleware:

```bash
from fastapi import FastAPI

app = FastAPI()


@app.middleware("http")
async def my_custom_middleware(request: Request, call_next):
    ... # Executa algo antes da requisição
    response = await call_next(request)  # Executa a requisição
    ... # Executa algo depois da requisição
    return response  # Retorna a resposta da requisição
```

Sempre que criarmos um middleware, precisamos informar 2 parâmetros:

* request: o objeto que representa a requisição HTTP
* call_next: a função que será executada para realizar a requisição (isto é: a função que representa a rota) ou o próximo middleware.

### Dependências

Outra forma de reaproveitar código entre rotas no FastAPI é usando dependências. Elas são funções que serão executadas antes de uma rota e podem ser usadas para, por exemplo, acrescentar parâmetros a uma requisição. Para criar uma dependência, basta criar uma função e registrá-la como parâmetro de uma rota:

```bash
from fastapi import Depends, FastAPI

app = FastAPI()


def my_dependency(query_string: str = None):
    ... # Executa algo antes da requisição
    return  query_string  # Retorna o valor para continuar requisição


@app.get("/")
async def my_route(dependency: str = Depends(my_dependency)):
    return {"message": dependency}
```

Nesse caso, o retorno da requisição GET "/?query_string=DependencyResult" será:

```bash
{
  "message": "DependencyResult"
}
```
