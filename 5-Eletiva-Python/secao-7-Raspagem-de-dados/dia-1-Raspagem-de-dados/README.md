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

</details>
</br>

<details>
<summary><strong> Rate Limit </strong></summary>


Muitas vezes a página de onde estamos removendo o conteúdo possui uma limitação de quantas requisições podemos enviar em um curto período de tempo, evitando assim ataques de negação de serviço.

Isto pode levar a um bloqueio por um curto período de tempo ou até mesmo banimento de acessar um recurso.

Que tal vermos um exemplo? 😎

```bash
import requests


# À partir da décima requisição somos bloqueados de acessar o recurso
# Código de status 429: Too Many Requests
for _ in range(15):
    response = requests.get("https://www.cloudflare.com/rate-limit-test/")
    print(response.status_code)
```

Neste exemplo, após a décima requisição, o servidor começa a nos retornar respostas com o código de status 429, “Too Many Requests”. Isto significa que estamos utilizando uma taxa de solicitação maior que a suportada. Ele permanecerá assim por algum tempo (1 minuto).

Uma boa prática é sempre fazermos uma pausa entre as requisições, ou lote delas, mesmo que o website onde a informação está não faça o bloqueio. Assim, evitamos tirar o site do ar.

```bash
import requests
import time


# Coloca uma pausa de 6 segundos a cada requisição
# Obs: este site de exemplo tem um rate limit de 10 requisições por minuto
for _ in range(15):
    response = requests.get("https://www.cloudflare.com/rate-limit-test/")
    print(response)
    time.sleep(6)
```

</details>
</br>

<details>
<summary><strong> Timeout </strong></summary>

Ás vezes pedimos um recurso ao servidor, mas caso o nosso tráfego de rede esteja lento ou exista um problema interno do servidor, nossa resposta pode demorar ou até mesmo ficar travada indefinidamente.

Como garantir, após um tempo, que o recurso seja retornado? 🤔

```bash
import requests

# Por 10 segundos não temos certeza se a requisição irá retornar
response = requests.get("https://httpbin.org/delay/10")
print(response)
```

Podemos definir um tempo limite (timeout) para que, após este tempo, possamos tomar alguma atitude, como por exemplo, realizar uma nova tentativa.

Este tempo limite normalmente é definido através de experimentações e análise do tempo de resposta normal de uma requisição.

```bash
import requests


try:
    # recurso demora muito a responder
    response = requests.get("http://httpbin.org/delay/10", timeout=2)
except requests.ReadTimeout:
    # vamos fazer uma nova requisição
    response = requests.get("http://httpbin.org/delay/1", timeout=2)
finally:
    print(response.status_code)
```

No exemplo acima, para efeitos didáticos, modificamos a URI do recurso, diminuindo o delay de resposta da requisição através do timeout, porém normalmente este valor não muda.

</details>
</br>

<details>
<summary><strong> Analisando respostas </strong></summary>

Para realizar a extração de dados de um conteúdo web vamos utilizar uma biblioteca chamada parsel. Ela pode ser instalada com o seguinte comando:

```bash
python3 -m pip install parsel
```

### Vamos para a prática? 💪

Como já aprendemos a realizar requisições HTTP e buscar conteúdo, vamos agora analisar este conteúdo e extrair informações.

Para ajudar na didática, vamos utilizar o site http://books.toscrape.com/. Ele é um site próprio para o treinamento de raspagem de dados.

Para começar, vamos acessar o site e ver o seu conteúdo.

Em código, vamos baixar o conteúdo da página e criar um seletor, que será utilizado para realizarmos as extrações. Vamos criar o arquivo .py para buscarmos as informações:

exemplo_scrape.py

```bash
from parsel import Selector
import requests


response = requests.get("http://books.toscrape.com/")
selector = Selector(text=response.text)
print(selector)
```

Ok, que tal extrairmos todos os livros desta primeira página e buscar seus títulos e preços?

Para conseguirmos extrair essas informações precisamos, primeiro, inspecionar cada um dos elementos, buscando algo que os identifique de forma única na página.

exemplo_scrape.py

```bash
# ...


# response = requests.get("http://books.toscrape.com/")
# selector = Selector(text=response.text)

# O título está no atributo title em um elemento âncora (<a>)
# Dentro de um h3 em elementos que possuem classe product_pod
titles = selector.css(".product_pod h3 a::attr(title)").getall()
# Estamos utilizando a::attr(title) para capturar somente o valor contido no texto do seletor

# Os preços estão no texto de uma classe price_color
# Que se encontra dentro da classe .product_price
prices = selector.css(".product_price .price_color::text").getall()

# Combinando tudo podemos buscar os produtos
# em em seguida buscar os valores individualmente
for product in selector.css(".product_pod"):
    title = product.css("h3 a::attr(title)").get()
    price = product.css(".price_color::text").get()
    print(title, price)
```

O seletor principal que contém todo o conteúdo da página pode ser utilizado em uma busca para encontrar seletores mais específicos. Podemos fazer isto utilizando a função css. Ela recebe um seletor CSS como parâmetro, embora podemos passar um tipo especial de seletor quando queremos algum valor bem específico como o texto ou um atributo.

Após definir o seletor, podemos utilizar a função get para buscar o primeiro seletor/valor que satisfaça aquela busca. A função getall é similar, porém traz todos os valores que satisfaçam aquele seletor.

Assim como temos a função css que faz a busca por seletores CSS, temos também a função xpath, que faz a busca com base em XPath.

👀 De olho na dica: existem sites que podem ajudar com seletores, como css ou xpath.

</details>
</br>

<details>
<summary><strong> Recursos paginados </strong></summary>

Tudo certo, temos 20 livros, mas sabemos que na verdade este site possui 1000 livros. Que tal coletarmos todos eles?!

Navegando um pouco por entre as páginas, percebemos que cada página possui uma referência para a próxima. Mas, se a URL é sequencial, por que não jogamos valores até a página avisar que o recurso não foi encontrado? 🤔

Acontece que podemos evitar fazer requisições desnecessárias, já que a página nos informa a próxima.

O que precisamos fazer é criar um seletor com a página, extrair os dados, buscar a nova página e repetir todo o processo, até termos navegados em todas as páginas.

Até a parte da extração nós já fizemos, vamos então dar uma olhada em como buscar a próxima página.

exemplo_scrape.py

```bash
# ...
# for product in selector.css(".product_pod"):
#     title = product.css("h3 a::attr(title)").get()
#     price = product.css(".price_color::text").get()
#     print(title, price)

# Existe uma classe next, que podemos recuperar a url através do seu elemento âncora
next_page_url = selector.css(".next a::attr(href)").get()
print(next_page_url)
```

Agora que sabemos como recuperar a próxima página, podemos iniciar na primeira página e continuar buscando livros enquanto uma nova página for encontrada. Cada vez que encontrarmos uma página, extraímos seus dados e continuamos até acabarem as páginas. Então vamos alterar tudo que tínhamos escrito no arquivo exemplo_scrape.py para o código abaixo:

exemplo_scrape.py

```bash
from parsel import Selector
import requests


# Define a primeira página como próxima a ter seu conteúdo recuperado
URL_BASE = "http://books.toscrape.com/catalogue/"
next_page_url = 'page-1.html'
while next_page_url:
    # Busca o conteúdo da próxima página
    response = requests.get(URL_BASE + next_page_url)
    selector = Selector(text=response.text)
    # Imprime os produtos de uma determinada página
    for product in selector.css(".product_pod"):
        title = product.css("h3 a::attr(title)").get()
        price = product.css(".price_color::text").get()
        print(title, price)
    # Descobre qual é a próxima página
    next_page_url = selector.css(".next a::attr(href)").get()
```

</details>
</br>

<details>
<summary><strong> Recursos obtidos à partir de outro recurso </strong></summary>

Agora que estamos coletando todos os livros, que tal coletarmos também a descrição de cada livro?

O problema é que a descrição só pode ser acessada navegando até a página específica de cada livro.

▶️ O primeiro passo é investigarmos como descobrir a URL que nos leva até a página de detalhes de um produto. 🔍

Com esse seletor em mãos, precisamos recuperar o atributo href que contém o link para a página de detalhes do livro. Vamos criar um outro arquivo, apenas para fazer o teste da feature que queremos implementar, depois vamos alterar o código do arquivo exemplo_scrape.py para realmente implementar a função.

⚠️Lembre-se de criar o arquivo no mesmo diretório que já estava utilizando.

teste.py

```bash
from parsel import Selector
import requests

URL_BASE = "http://books.toscrape.com/catalogue/"

# Vamos testar com a primeira página
response = requests.get(URL_BASE + "page-1.html")
selector = Selector(text=response.text)

# Recupera o atributo href do primeiro elemento que combine com o seletor
href = selector.css(".product_pod h3 a::attr(href)").get()
print(href)

# Para obter a url completa, basta adicionar a nossa URL_BASE
print(URL_BASE + href)
```

▶️ Em seguida, acessamos a página de detalhes do produto, e inspecionamos a descrição do produto.

▶️ A descrição do produto está uma tag p, “irmã” de uma tag com id product_description. Isto pode ser expresso através do seletor a.

No código, precisamos realizar uma nova requisição à página de detalhes e depois analisaremos seu conteúdo em busca da descrição do produto. Para isso, vamos alterar todo o conteúdo novamente, porém dessa vez será o conteúdo do arquivo teste.py:

teste.py

```bash
from parsel import Selector
import requests

URL_BASE = "http://books.toscrape.com/catalogue/"

response = requests.get(URL_BASE + "page-1.html")
selector = Selector(text=response.text)

href = selector.css(".product_pod h3 a::attr(href)").get()
detail_page_url = URL_BASE + href

# baixa o conteúdo da página de detalhes
detail_response = requests.get(detail_page_url)
detail_selector = Selector(text=detail_response.text)

# recupera a descrição do produto
# ~ significa a tag irmã
description = detail_selector.css("#product_description ~ p::text").get()
print(description)
```

▶️ Por fim, vamos adicionar a lógica para buscar a descrição do produto no nosso código existente:

exemplo_scrape.py

```bash
# from parsel import Selector
# import requests


# URL_BASE = "http://books.toscrape.com/catalogue/"
# Define a primeira página como a próxima a ter seu conteúdo recuperado
# next_page_url = 'page-1.html'
while next_page_url:
    # Busca o conteúdo da próxima página
    # response = requests.get(URL_BASE + next_page_url)
    # selector = Selector(text=response.text)
    # Imprime os produtos de uma determinada página
    for product in selector.css(".product_pod"):
        # Busca e extrai o título e  o preço
        # title = product.css("h3 a::attr(title)").get()
        # price = product.css(".price_color::text").get()
        # print(title, price)

        # Busca o detalhe de um produto
        detail_href = product.css("h3 a::attr(href)").get()
        detail_page_url = URL_BASE + detail_href

        # Baixa o conteúdo da página de detalhes
        detail_response = requests.get(detail_page_url)
        detail_selector = Selector(text=detail_response.text)

        # Extrai a descrição do produto
        description = detail_selector.css("#product_description ~ p::text").get()
        print(description)

    # Descobre qual é a próxima página
    # next_page_url = selector.css(".next a::attr(href)").get()
```

</details>
</br>

<details>
<summary><strong> Limpeza de dados </strong></summary>


🧼🧽 Estamos extraindo nossos dados, porém estes dados contém algumas “sujeiras” que podem atrapalhar nossas análises. Por exemplo, pare pra olhar o preço do livro, viu algo diferente? O preço possui um caractere estranho Â£26.08 antes do seu valor. E a descrição do livro que contém o sufixo ...more.

Seria conveniente, antes de estruturar e armazenar estes dados, que fizéssemos uma limpeza neles.

No caso do valor, poderíamos utilizar uma expressão regular para remover os outros caracteres. O padrão é conter um símbolo de libra, seguido por números, ponto para separar casas decimais e dois números como casas decimais. Essa expressão regular pode ser feita da seguinte forma: £\d+\.\d{2}.

Agora, para utilizar a expressão regular que fizemos, podemos substituir o método getall pelo método re, ou o método get por re_first. Ambos, além de recuperar valores, aplicarão a expressão regular sobre aquele valor.

Vamos primeiro fazer essas features, novamente, no arquivo de teste.py para vermos funcionando. Depois vamos implementá-las no arquivo exemplo_scrape.py:

teste.py

```bash
from parsel import Selector
import requests


response = requests.get("http://books.toscrape.com/")
selector = Selector(text=response.text)
# Extrai todos os preços da primeira página
prices = selector.css(".product_price .price_color::text").re(r"£\d+\.\d{2}")
print(prices)
```

Já para o caso do sufixo ...more, poderíamos utilizar fatiamento para removê-lo. Mas antes é importante verificarmos se o conteúdo possui o sufixo, evitando assim perda de conteúdo de forma acidental. Vamos ver como isso funciona no arquivo teste.py:

teste.py

```bash
from parsel import Selector
import requests


response = requests.get("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
selector = Selector(text=response.text)

# Extrai a descrição
description = selector.css("#product_description ~ p::text").get()
print(description)

# "Fatiamos" a descrição removendo o sufixo
suffix = "...more"
if description.endswith(suffix):
    description = description[:-len(suffix)]
print(description)
```

Alguns outros exemplos de “sujeiras” são valores que contém tabulações, quebras de linha ou conteúdo além do esperado.

Agora vamos implementar essas funcionalidades no nosso arquivo exemplo_scrape.py:

exemplo_scrape.py

```bash
from parsel import Selector
import requests


# URL_BASE = "http://books.toscrape.com/catalogue/"
# Define a primeira página como próxima a ter seu conteúdo recuperado
# next_page_url = 'page-1.html'
# while next_page_url:
    # Busca o conteúdo da próxima página
    # response = requests.get(URL_BASE + next_page_url)
    # selector = Selector(text=response.text)
    # Imprime os produtos de uma determinada página
    # for product in selector.css(".product_pod"):
        # Busca e extrai o título e  o preço
        # title = product.css("h3 a::attr(title)").get()
        price = product.css(".product_price .price_color::text").re(r"£\d+\.\d{2}")
        # print(title, price)

        # Busca o detalhe de um produto
        # detail_href = product.css("h3 a::attr(href)").get()
        # detail_page_url = URL_BASE + detail_href

        # Baixa o conteúdo da página de detalhes
        # detail_response = requests.get(detail_page_url)
        # detail_selector = Selector(text=detail_response.text)

        # Extrai a descrição do produto
        # description = detail_selector.css("#product_description ~ p::text").get()
        suffix = "...more"
        if description.endswith(suffix):
            description = description[:-len(suffix)]
        # print(description)

    # Descobre qual é a próxima página
    # next_page_url = selector.css(".next a::attr(href)").get()
```

👀 De olho na dica: Strings em Python possuem vários métodos para ajudarem nesta limpeza, como por exemplo, o strip. Para ler a documentação e procurar esses métodos, execute help(str) no seu terminal interativo.

</details>
</br>

<details>
<summary><strong> Fatiamento </strong></summary>

Estruturas de dados do tipo sequência, como listas, tuplas e strings, podem ter seus elementos acessados através de um índice:

```
# Recupera o primeiro elemento
[1, 2, 3][0]  # Saída: 1
```

Podemos também definir dois índices que serão o valor inicial e final de uma subsequência da estrutura. Ou três valores, sendo o último o tamanho do passo que daremos ao percorrer a subsequência:

```bash
# Quando não incluso o valor inicial, iniciaremos do índice 0
# e do índice 2 em diante, os elementos não são incluídos
(1, 2, 3, 4)[:2]  # Saída: (1, 2)

# Quando omitimos o valor final
# o fatiamento ocorre até o fim da sequência
(1, 2, 3, 4)[1:]  # Saída: (2, 3, 4)

# Vá do índice 3 até o 7.
# O item no índice 7 não é incluído
"palavra"[3:7]  # Saída: "avra"

# Começando do elemento de índice 1, vá até o último,
# saltando de 2 em 2
[1, 2, 3, 4][1::2]  # Saída: [2, 4]
```

Chamamos esta operação de fatiamento. Ela é muito utilizada para obtermos uma subsequência de uma sequência.

⚠️À partir da versão 3.9 do Python, teremos uma função chamada removesuffix, que é equivalente à palavra[:-len(suffix)].

</details>
</br>

<details>
<summary><strong> Scrapy </strong></summary>

🕷 Uma excelente e poderosa ferramenta para raspagem de dados é a Scrapy. Ela possui, em sua implementação, todos os mecanismos citados anteriormente e outros recursos adicionais.

https://scrapy.org/

Vale a pena dar uma olhadinha! 😉

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