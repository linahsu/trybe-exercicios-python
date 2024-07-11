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