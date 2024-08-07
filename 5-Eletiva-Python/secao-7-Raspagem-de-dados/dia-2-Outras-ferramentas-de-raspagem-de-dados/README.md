# Selenium

Essencialmente, o Selenium é um conjunto de ferramentas para automação de navegadores da web, que permite controlar remotamente instâncias de navegadores e emular a interação de um usuário com o navegador.

No núcleo do Selenium está o WebDriver, uma API e protocolo que define uma interface para controlar o comportamento dos navegadores web. É através do WebDriver que o Selenium suporta a automação dos principais navegadores do mercado.

Cada navegador possui uma implementação específica do WebDriver, chamada de driver, que é o componente responsável por delegar e manipular a comunicação entre o Selenium e o navegador.

Para utilizar o Selenium é necessário instalar as bibliotecas de acordo com a linguagem que você utilizará, além de ter instalado o navegador que deseja usar e o driver correspondente para ele.

Após essas instalações, com apenas algumas linhas de código podemos criar uma instância de navegador para simular um acesso real a um site, como uma pessoa utilizando o browser faria.

Essa função pode ser extremamente útil quando falamos de raspagem de dados, pois em Single Page Applications, por exemplo, como sites construídos em React, só após uma requisição para a página é que o conteúdo será montado e as informações estarão disponíveis para serem consultadas. Simulando um acesso de uma pessoa real ao site, o Selenium pode evitar que o resultado da consulta volte vazio nesses casos.

Por exemplo, se você usar a biblioteca requests para fazer uma requisição do tipo get em um site feito em React, você vai receber de volta um HTML relativamente simples, somente com um elemento root e um código JavaScript grande, que seria o responsável por criar dinamicamente a página web. Acontece que esse código JavaScript não é rodado pelo Python, permanecendo apenas um texto, fazendo com que sua página nunca seja montada e que você não ache as informações que desejava. Já o Selenium cria uma instância de um navegador, por exemplo o Firefox, e de fato executa o JavaScript como se fosse uma pessoa acessando o site pelo navegador normalmente, e somente após o site terminar de carregar é que o scrape é feito.

## Instalação do Selenium

Podemos utilizar o Selenium tanto instalado diretamente em nossa máquina, quanto através de um container Docker. A seguir teremos o passo a passo das duas formas de instalação da ferramenta, mas você precisa seguir apenas uma delas, a escolha fica inteiramente a seu critério, para conseguir executar o exemplo desenvolvido ao longo do conteúdo.

Independentemente da forma escolhida, lembre-se de criar um ambiente virtual antes de instalar bibliotecas.

<details>
<summary><strong> Instalação utilizando o Docker </strong></summary>

Ao optar por essa instalação, é essencial ter o Docker instalado em seu computador. Para consultar como fazer a instalação você pode acessar este conteúdo.

A imagem que utilizaremos do Selenium é a selenium/standalone-firefox:

```bash
docker pull selenium/standalone-firefox:106.0
```

### Em computadores MacOS com o chip M1

A imagem Docker recomendada há pouco pode não funcionar corretamente em computadores MacOS com o chip M1. Se este for o caso da sua máquina, você pode utilizar a imagem seleniarm/standalone-firefox:

```bash
docker pull seleniarm/standalone-firefox:105.0
```

### Iniciando a imagem Docker

Para efetivamente começar a utilizar o Selenium, precisaremos inicializar a imagem Docker que baixamos anteriormente. Na documentação da imagem recomendada anteriormente às pessoas que utilizam Linux ou MacOS sem o novo processador M1, especificamente na seção Using your browser (no VNC client is needed), que permite a inspeção visual da atividade do container através do navegador, encontramos os comandos que utilizaremos a seguir.

Faremos uma única adaptação, que é acrescentar a flag --name para nomear o container e facilitar sua manipulação.

```bash
docker run -d -p 4444:4444 -p 7900:7900 --shm-size 2g --name firefox selenium/standalone-firefox:106.0
```

As flags utilizadas acima têm as seguintes finalidades:

* -d serve para rodar o container em segundo plano
* -p vincula uma porta do SO a outra porta dentro do container
* --shm-size aumenta o limite de quantidade de memória compartilhada com o container
* --name define qual vai ser o nome do container
* --platform (somente se utilizado) diz ao docker qual a plataforma deve ser usada

Pessoas que utilizam MacOS com o chip M1, podem consultar a documentação da imagem recomendada aqui. Neste caso, o comando a ser utilizado será levemente diferente do apresentado há pouco:

```bash
docker run -d --name firefox -p 4444:4444 -p 7900:7900 --shm-size 2g seleniarm/standalone-firefox:105.0
```

Acessando o navegador Firefox na porta 7900, poderemos conferir se o container está rodando corretamente. Conforme a documentação, será necessário apenas utilizar a senha secret para ter acesso ao container.

⚠️ Atenção: Caso aconteça de o container travar, basta que você o reinicie, com o comando:

```bash
docker restart firefox
```

</details>
</br>

<details>
<summary><strong> Instalação local </strong></summary>

Para fazer a instalação do Selenium diretamente em sua máquina, basta executar o comando a seguir em seu terminal:

```bash
pip3 install selenium
```

Neste exemplo, vamos utilizar a versão 4.6.0, que pode ser instalada com o seguinte comando:

```bash
pip3 install selenium==4.6.0
```

Como dito anteriormente, para utilizar a ferramenta é necessário também instalar o driver do browser que utilizaremos. Nesta parte da documentação (https://www.selenium.dev/documentation/webdriver/troubleshooting/errors/driver_location/) você encontra os links para os drivers dos principais browsers. Para este exemplo utilizaremos o Mozilla Firefox (especificamente na versão 106.0), que já vem instalado na maioria das distribuições Linux, mas a utilização de outros navegadores, como o Chrome, é bem similar.

Após escolher o browser que será utilizado, clique em Downloads, e depois do redirecionamento para a página do github com as opções do geckodriver, clique na versão compatível com o sistema operacional instalado em seu computador.

⚠️ Caso vá utilizar o Chrome, o link de Download redirecionará para uma página com diversas versões do driver. Neste caso, clique na opção compatível com a versão do navegador que você tem instalada e em seguida escolha a versão compatível com seu sistema operacional. Para consultar a versão do Chrome, basta ir em seu navegador, nos três pontinhos na parte superior direita da barra de tarefas, clicar em ‘Ajuda’ (help) e em seguida em ‘Sobre o Google Chrome’ (About Google Chrome).

⚠️ Caso esteja fazendo o download via linha de comando, você pode utilizar o utilitário wget. Para baixar o geckodriver-v0.32.0 para o Firefox, o comando é wget https://github.com/mozilla/geckodriver/releases/download/v0.32.0/geckodriver-v0.32.0-linux64.tar.gz (observe que esta é a versão para Linux). Para extrair o driver você pode utilizar utilitário tar. Outras versões do geckodriver para outros sistemas operacionais podem ser encontradas aqui. ⚠️ Atenção: é essencial que tanto o driver quanto o navegador estejam no path.**

Nas distros Linux e no MacOS, o próximo passo é extrair o arquivo baixado e movê-lo para o diretório ‘/usr/bin’. Para isso, abra no terminal o diretório onde está o arquivo recém baixado e utilize o comando:

```bash
sudo mv geckodriver /usr/bin
```

Caso você esteja em um ambiente virtual, o diretório bin do ambiente é adicionado ao path automaticamente, então você pode mover o binário para lá:

```bash
mv geckodriver .venv/bin/
```

Além disso, você pode simplesmente copiar e colar ou até mesmo arrastar e soltar o arquivo geckodriver dentro do diretório /bin em seu ambiente virtual.
</details>
</br>

<details>
<summary><strong> Primeiros passos com o Selenium </strong></summary>

Vamos criar um arquivo para fazer nossos primeiros experimentos com o Selenium! 🚀

👀 De olho na dica: é importante evitar utilizar os nomes das bibliotecas e ferramentas para nomear os arquivos.

⚠️ Para que o código do exemplo funcione, lembre-se que é necessário ter o Firefox instalado no seu computador.

Agora vamos colocar a mão na massa! Crie o seguinte arquivo:

selenium_example.py

```bash
# importação do webdriver, que é o que possibilita a implementação para todos
# os principais navegadores da web
from selenium import webdriver

# criação de uma instância de navegador utilizando o Firefox
firefox = webdriver.Firefox()

# requisições para essa instância criada utilizando o método `get`
response = firefox.get("https://www.python.org/")
```

Caso você esteja utilizando o Selenium com Docker, seu código inicial será um pouco diferente, pois precisamos passar algumas opções e utilizar o método remote para vincular nosso arquivo de código ao container rodando na porta 7700. Portanto, seu código inicial ficará assim:

selenium_example.py

```bash
# importação do webdriver, que é o que possibilita a implementação para todos
# os principais navegadores da web
from time import sleep
from selenium import webdriver

# Para usar o chrome ao invés do firefox trocamos FirefoxOptions por ChromeOptions
# Todavia, caso esteja utilizando o docker, atente-se ao container sendo utilizado.
options = webdriver.FirefoxOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--start-maximized')

firefox = webdriver.Remote(command_executor="http://localhost:4444/wd/hub", options=options)

# requisições para essa instância criada utilizando o método `get`
response = firefox.get("https://www.python.org/")

# espera 10 segundos
sleep(10)

# encerra o navegador, importante quando usamos containers
firefox.quit()
```

Daqui para frente, utilizaremos como base o código em que a instalação foi feita diretamente na máquina, por isso tenha atenção nas linhas que trazem as options e a que faz a definição de firefox, pois elas não poderão ser removidas no caso de você estar utilizando Docker. O restante do código pode seguir as instruções dos próximos passos normalmente.

Executando o código acima, você verá que uma janela do navegador abrirá automagicamente no site solicitado. Se você reparar, um ícone aparece na barra de endereço do navegador e se você passar o mouse por cima verá a mensagem “Browser is under remote control (reason: Marionette)”.

Caso você esteja utilizando o Selenium com Docker, todas as ações executadas serão vistas na janela do Firefox no endereço http://localhost:7900.

⚠️ A partir deste momento, o ideal é que é você abra os endpoints dos exemplos e inspecione as páginas para entender como a página está estruturada e compreender melhor porque estamos pegando cada informação daquela maneira. Além de ajudar no aprendizado, isso é importante porque estamos utilizando páginas reais da web, que estão recebendo manutenção e atualizações constantes. Isso significa que um campo utilizado no exemplo e que existe na página hoje, pode não existir mais no site daqui a um mês. Trabalhando com web scraping, essa atenção é essencial! 😉

Você pode instruir o navegador a realizar diversas operações através do código. Para dar um exemplo e evidenciar o potencial do Selenium, com apenas três linhas conseguimos fazer com que logo após abrir o navegador, algo seja digitado no campo de pesquisa e o selenium pressione enter para efetivar a busca:

```bash
# from selenium import webdriver
from selenium.webdriver.common.keys import Keys # Importa teclas comuns

# firefox = webdriver.Firefox()

response = firefox.get("https://www.google.com.br/")

# pesquisa na instância aberta do navegador pela primeira ocorrência
# do nome 'q'
search_input = firefox.find_element("name", "q")

# escreve selenium dentro do campo de pesquisa
search_input.send_keys("selenium")

# pressiona enter para realizar a busca
search_input.send_keys(Keys.ENTER)
```

Partindo para a parte que nos interessa, a de web scraping, vamos juntar os conhecimentos da última aula ao que já vimos hoje e pegar algumas informações dos livros de uma página dedicada para treinar scraping.

O Selenium tem vários métodos públicos, como o find_element que usamos anteriormente e o find_elements (no plural), utilizados para localizar o primeiro elemento correspondente ao resultado do filtro ou todos os elementos que se encaixarem na busca, respectivamente.

Também podemos utilizar o By para especificar um elemento CSS ou XPATH que será buscado, para isso é necessário importá-lo via:

```bash
from selenium.webdriver.common.by import By
```

Nesse caso, devemos passar dois parâmetros: o primeiro parâmetro define o que você irá buscar e o segundo o filtro da nossa pesquisa. Abaixo temos duas opções no que diz respeito ao que estamos buscando, uma delas utilizando o By e a outra no formato previamente utilizado (quando buscamos pelo campo de nome q no exemplo acima).

```bash
Com o By	            Sem o By
By.ID	                “id”
By.NAME	                “name”
By.XPATH	            “xpath”
By.LINK_TEXT	        “link text”
By.PARTIAL_LINK_TEXT	“partial link text”
By.TAG_NAME         	“tag name”
By.CLASS_NAME	        “class name”
By.CSS_SELECTOR	        “css selector”
```

Assim como quando utilizamos a lib requests, inspecionar a página que queremos raspar é imprescindível para entendermos a estrutura de como a página foi montada e quais elementos devemos selecionar para buscar as informações que queremos.

scrape_selenium.py

```bash
from selenium import webdriver

# Importa o By
from selenium.webdriver.common.by import By

firefox = webdriver.Firefox()

firefox.get("https://books.toscrape.com/")


# Define a função que fará o scrape da URL recebida
def scrape(url):
    firefox.get(url)

    # Itera entre os elementos com essa classe
    for book in firefox.find_elements(By.CLASS_NAME, "product_pod"):
        # Cria dict vazio para guardar os elementos capturados
        new_item = {}

        # Cria uma chave 'title' no dict que vai receber o resultado da busca
        # O título está em uma tag anchor que está dentro de uma tag 'H3'
        new_item["title"] = (
            book.find_element(By.TAG_NAME, "h3")
            .find_element(By.TAG_NAME, "a")
            .get_attribute("innerHTML")
        )

        # O preço do book está em um elemento da classe 'price_color'
        new_item["price"] = book.find_element(
            By.CLASS_NAME, "price_color"
        ).get_attribute("innerHTML")

        # O link está dentro de um atributo 'href'
        new_item["link"] = (
            book.find_element(By.CLASS_NAME, "image_container")
            .find_element(By.TAG_NAME, "a")
            .get_attribute("href")
        )

        print(new_item)


scrape("https://books.toscrape.com/")
```

Utilizamos bastante no código acima o método get_attribute. A razão disso é que com o Selenium, o elemento retornado depois da busca pelo atributo CSS será do tipo webdriver e não texto. É justamente para fazer essa conversão que utilizamos esse método especificando o atributo ‘innerHTML’ ou ‘href’, por exemplo.

Também utilizamos o método find_element encadeado para procurar um elemento dentro de outro elemento, como fizemos para pegar o link, por exemplo, que era um elemento âncora dentro de uma div.

Certo, mas até agora só pegamos informações dos livros da primeira página do site, como fazemos para pegar todos os livros, até a última página? 🤔

1. Primeiro precisamos organizar nosso código e determinar que o retorno da função scrape salve o resultado da raspagem em uma lista.
2. Em seguida, temos que criar uma nova lista para abrigar os dados de uma página;
3. Depois devemos acessar o botão para ir para a próxima página e lá refazer o processo de salvar todas as informações solicitadas, repetindo esse mecanismo até todas as páginas serem percorridas.

Vamos ver como fazer isso com Selenium?

```bash
# from selenium import webdriver

# from selenium.webdriver.common.by import By


# firefox = webdriver.Firefox()


# def scrape(url):
#     firefox.get(url)

    books = []

#     for book in firefox.find_elements(By.CLASS_NAME, "product_pod"):
#         new_item = {}

#         new_item["title"] = (
#             book.find_element(By.TAG_NAME, "h3")
#             .find_element(By.TAG_NAME, "a")
#             .get_attribute("innerHTML")
#         )

#         new_item["price"] = book.find_element(
#             By.CLASS_NAME, "price_color"
#         ).get_attribute("innerHTML")

#         new_item["link"] = (
#             book.find_element(By.CLASS_NAME, "image_container")
#             .find_element(By.TAG_NAME, "a")
#             .get_attribute("href")
#         )

        books.append(new_item)
    return books

firefox.get("https://books.toscrape.com/")

all_books = []
url2request = "https://books.toscrape.com/"

# Cria uma variável com o seletor que captura o link do botão de passar para
# a próxima página
next_page_link = (
    firefox.find_element(By.CLASS_NAME, "next")
    .get_attribute("innerHTML")
)

# Enquanto este botão de 'next' existir na página ele irá iterar
while next_page_link:

    # Usa o método extend para colocar todos os elementos de uma lista dentro
    # de outra
    all_books.extend(scrape(url2request))
    url2request = (
        firefox.find_element(By.CLASS_NAME, "next")
        .find_element(By.TAG_NAME, "a")
        .get_attribute("href")
    )

print(all_books)
```

Como há muitas páginas a serem percorridas, é normal que a execução deste código leve alguns minutos. 😉

Observando o navegador aberto com a execução do código, você verá que ele abriu na página solicitada e em seguida começou a percorrer as páginas do site, o que indica que tudo está correndo bem. Contudo, pouco antes de finalizar, já na última página, no terminal aparece uma exceção do Selenium chamada ‘NoSuchElementException’.

Pela mensagem fica mais fácil de entender o que deu errado. Ao entrar na última página, ele fez a raspagem de todas as informações pedidas, porém o passo seguinte foi impossível de executar já que precisava achar o botão ‘next’ para alterar o link na variável url2request. A forma mais simples de resolver este erro é importar a exceção do Selenium e tratá-la com um try, de forma que ao ocorrer esta situação o loop seja quebrado.

```bash
# from selenium import webdriver

# from selenium.webdriver.common.by import By

# from selenium.common.exceptions import NoSuchElementException

# firefox = webdriver.Firefox()


# def scrape(url):
#     firefox.get(url)

#     books = []

#     for book in firefox.find_elements(By.CLASS_NAME, "product_pod"):
#         new_item = {}

#         new_item["title"] = (
#             book.find_element(By.TAG_NAME, "h3")
#             .find_element(By.TAG_NAME, "a")
#             .get_attribute("innerHTML")
#         )

#         new_item["price"] = book.find_element(
#             By.CLASS_NAME, "price_color"
#         ).get_attribute("innerHTML")

#         new_item["link"] = (
#             book.find_element(By.CLASS_NAME, "image_container")
#             .find_element(By.TAG_NAME, "a")
#             .get_attribute("href")
#         )

#         books.append(new_item)
#     return books


# firefox.get("https://books.toscrape.com/")

# all_books = []
# url2request = "https://books.toscrape.com/"

# next_page_link = (
#     firefox.find_element(By.CLASS_NAME, "next")
#     .get_attribute("innerHTML")
# )

# while next_page_link:

#     all_books.extend(scrape(url2request))
    try:
        url2request = (
            firefox.find_element(By.CLASS_NAME, 'next')
            .find_element(By.TAG_NAME, 'a').get_attribute('href')
        )
    except NoSuchElementException:
        print("exception handled")
        break

# print(all_books)
```

Agora sim, após uma eternidade percorrer todas as páginas do site temos as informações que queremos de todos os 1000 livros lá existentes! 🥳

Antes de partirmos para a próxima ferramenta que veremos hoje, aqui vai uma última dica: é muito legal ver o navegador abrir e executar os comandos que definimos, porém quando não precisamos ou não queremos ver essa execução, podemos evitá-la utilizando as options. Basta importá-las do webdriver, adicionar um novo argumento com a opção que deseja e depois passá-la como parâmetro para a instância de navegador criada.

```bash
from selenium import webdriver
# Importa a classe 'Options' do browser
from selenium.webdriver.firefox.options import Options


firefox = webdriver.Firefox()

# Instancia um objeto da classe 'Options'
options = Options()
# Adiciona um argumento passando o parâmetro '--headless'
options.add_argument('--headless')

# Define que a instância do navegador deve usar as options definidas
firefox = webdriver.Firefox(options=options)

# firefox.get('https://books.toscrape.com/')

# ...
```

💡 Caso queira explorar outras possibilidades oferecidas pelas options, você pode consultar este link da documentação. Ele redireciona para as opções disponíveis para o Firefox, mas na mesma página você encontra menus para consultar sobre outros navegadores.
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