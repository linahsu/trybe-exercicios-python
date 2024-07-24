# Getting started

<details>
<summary><strong> Preparando o ambiente </strong></summary>

Caso a versão do Python seja inferior a 3.10, você precisará atualizar o Python. Para isso, você pode utilizar o Pyenv, basta seguir nosso tutorial do Guia de configuração de ambiente. Isso é necessário porque mais à frente utilizaremos uma biblioteca que não funciona bem com a versão 3.9 ou inferiores do Python.

Para começar, vamos criar um novo diretório para o nosso projeto e entrar nele:

```bash
mkdir ecommerce && cd ecommerce
```

Em seguida, vamos criar um ambiente virtual para o nosso projeto e ativá-lo:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Agora, vamos instalar o Django:

```bash
pip install django
```

E, finalmente, vamos iniciar um projeto chamado ecommerce, no diretório atual:

```bash
django-admin startproject ecommerce .
```

Simples assim e nosso primeiro projeto foi criado! 🎉
</details>
</br>


<details>
<summary><strong> Executando o projeto </strong></summary>


Para executar o projeto, basta executar o comando:

```bash
python3 manage.py runserver
```

o Django possui algumas migrations internas que ainda não foram aplicadas ao banco de dados. Para aplicá-las, abra um novo terminal, ative o ambiente virtual e execute o comando:

```bash
python3 manage.py migrate
```
</details>
</br>

<details>
<summary><strong> Estrutura do projeto </strong></summary>

Passando rapidamente por cada um dos arquivos dentro do diretório ecommerce, que é o diretório do projeto em si, temos os arquivos:

* manage.py: é o arquivo usado internamente quando executamos comandos do Django - como o runserver que executamos anteriormente.
* __init__.py: arquivo que indica que o diretório é um pacote Python - já utilizamos este arquivo lá na seção 1, lembra? 😉
* asgi.py: arquivo de configuração do ASGI (Asynchronous Server Gateway Interface), que é o protocolo usado pelo Django para comunicação entre servidores web e aplicações web para lidar com solicitações assíncronas e em tempo real.
* settings.py: arquivo de configuração do projeto, que contém todas as configurações do Django para o projeto. É aqui que configuramos, por exemplo, o banco de dados que será usado, o idioma padrão da aplicação, etc. Veremos este arquivo com mais atenção daqui a pouco. 🤓
* urls.py: arquivo de configuração de rotas do projeto. Vamos explorar este arquivo com mais detalhes em breve. 🤩
* wsgi.py: arquivo de configuração do WSGI (Web Server Gateway Interface), que é o protocolo usado pelo Django para comunicação entre servidores web e aplicações web para lidar com solicitações HTTP.
* __pycache__: diretório que contém arquivos gerados automaticamente pelo Python para otimizar o carregamento de módulos.

#### Dois arquivos valem uma atenção especial: settings.py e urls.py. Bora dar uma olhada neles?

#### Arquivo settings.py

Este é o arquivo que reúne as principais configurações do projeto, com várias dessas configurações já definidas com valores-padrão. Vamos entender melhor algumas dessas configs?

* SECRET_KEY é uma chave de segurança que o Django utiliza para criptografar dados sensíveis, como senhas de pessoas usuárias, por exemplo. Ela já vem com um valor por padrão, mas explicitamente dada como insegura e por isso, é recomendável substitui-la por uma chave personalizada forte, especialmente em ambientes de produção.
* DEBUG é um booleano que indica se o modo de depuração (debug) está ativado ou não. Durante o desenvolvimento, ter esse modo ativado é muito útil para ajudar a identificar e corrigir bugs, o valor default (padrão) dessa variável é true justamente por isso. Contudo, ele pode trazer algumas vulnerabilidades à segurança, como, por exemplo, mostrar informações sensíveis do projeto - algo ruim se mostrado para uma pessoa usuária. Por isso, é importante que ele esteja desativado quando o projeto estiver em produção.
* ALLOWED_HOSTS é uma lista de nomes de domínios, subdomínios ou endereços IP que o Django permite que acessem o projeto. Você pode usar o valor '*', caso queira dar acesso a todos, ou definir uma lista com os grupos que terão acesso ao projeto, por exemplo, ['exemplo.com', 'subdomínio.exemplo.com', '192.168.1.1'].
* INSTALLED_APPS é uma lista de apps que serão acoplados no projeto Django. Alguns já vêm instalados por padrão, mas os apps criados por você para o projeto podem compor essa variável também. Veremos como fazer isso em breve! 🤩
* MIDDLEWARE é uma lista de middlewares que o Django utiliza para fazer algumas coisas como, por exemplo, o middleware de autenticação de pessoa usuária. Sua lógica é similar a dos Middlewares do Express, mas entraremos em detalhes sobre eles apenas na próxima seção.
* TEMPLATES é uma lista de diretórios em que o Django irá procurar por templates HTML.
DATABASES é a configuração de banco de dados do projeto. Como o Django já vem com o SQLite instalado por padrão, ele já vem com a configuração do SQLite, mas podemos trocar por outros.
* LANGUAGE_CODE é a configuração de idioma padrão do projeto. Por padrão, ele vem com o inglês, mas podemos alterar para qualquer outro.

De olho na dica 👀: você pode alterar a linguagem padrão do projeto Django para português apenas, alterando a variável language_code para pt-br. Experimente fazer isso e atualizar a página para ver a tela inicial está traduzida! 🤩

#### Arquivo urls.py

Já acessamos a rota raiz do projeto quando rodamos o servidor e acessamos a URL localhost:8000. Apesar de não termos definido nenhuma rota até aquele momento, a URL raiz já traz por padrão um retorno visual: uma página com o foguetinho informando que deu tudo certo com a instalação.

Como dito anteriormente, este arquivo reúne as rotas do projeto, com alguns valores já definidos por padrão. Vamos entender melhor como uma rota é definida?

A primeira coisa que temos é a função path, que define uma rota. Como parâmetro ela recebe a URL que será acessada e a função que será executada quando a URL for acessada.

Uma surpresa é que já temos uma rota definida no arquivo, a admin/, que é a interface administrativa que o Django fornece para o projeto. Vamos explorar ela com mais detalhes em breve. 😎
</details>
</br>

<details>
<summary><strong> Usando outro banco de dados </strong></summary>

Você pode iniciar apagando o arquivo db.sqlite3 do seu projeto, pois ele não será mais utilizado. Faremos as alterações no projeto para que ele use como banco de dados nosso conhecido MySQL, via Docker.

Para isso, o primeiro passo é alterar a variável DATABASE, no arquivo settings.py, para que ela tenha as configurações de acesso ao banco necessárias. De acordo com a documentação, a variável deve ficar assim:

```bash
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'ecommerce_database',
        'USER': 'root',
        'PASSWORD': 'password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
      }
}
```

Em seguida, criaremos um arquivo que conterá o script SQL que criará o banco de dados ecommerce_database. Ele ficará dentro do diretório ./database:

```bash
mkdir database && cd database
touch 01_create_database.sql
```

Por ora, o banco de dados não terá nenhuma tabela, portanto, o script de criação do banco de dados ecommerce_database deve ficar assim:

```bash
CREATE DATABASE IF NOT EXISTS ecommerce_database;

USE ecommerce_database;
```

Com isso feito, é hora de criar um arquivo Dockerfile na raiz do projeto (no mesmo nível do arquivo manage.py), com o seguinte conteúdo:

```bash
FROM mysql:8.0.32

ENV MYSQL_ROOT_PASSWORD password

# Copia o script SQL que acabamos de criar para um determinado diretório no container
COPY ./database/01_create_database.sql /docker-entrypoint-initdb.d/data.sql01
```

Para buildar a imagem, basta rodar o comando dentro da pasta do projeto que contém o arquivo Dockerfile.

```bash
docker build -t ecommerce-db .
```
Para executar o container e o script de criação do banco copiado no Dockerfile, é preciso passar algumas as variáveis de acesso definidas na variável DATABASES, do arquivo settings.py, para o container. Para isso, vamos usar o comando:

```bash
docker run -d -p 3306:3306 --name=ecommerce-mysql-container -e MYSQL_ROOT_PASSWORD=password -e MYSQL_DATABASE=ecommerce_database ecommerce-db
```

Neste momento, você já pode acessar o banco de dados pelo Workbench e verificar se ele foi criado corretamente.

Mas ainda não acabou! Lembra das migrations iniciais que geraram o famigerado aviso em vermelho no início do projeto? Elas ainda não foram executadas neste banco de dados. Para isso, é preciso executar o comando migrate do Django, mas antes instalar o mysqlclient:

```bash
pip install mysqlclient && python3 manage.py migrate
```

Caso ocorra algum erro no comando anterior, pode ser porque um pacote adicional chamado pkg-config não esteja instalado. Nesse caso, tente seguir todos os passos sugeridos pela documentação oficial do mysqlclient para a instalação do pacote. Para facilitar, o seguinte comando funciona para a maioria dos sistemas Linux:

```bash
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential pkg-config
```
</details>
</br>

<details>
<summary><strong> Criando a primeira aplicação </strong></summary>

Já criamos nosso projeto, agora chegou a hora de criar nossa primeira aplicação!

Vamos começar voltando no arquivo settings.py e adicionando o app que iremos criar à lista preexistente:

```bash
# ecommerce/ecommerce/settings.py

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
+    "products",
]
```

Com isso feito, é hora de efetivamente criar o app. O comando é similar ao utilizado para criar o projeto, mas agora vamos utilizar startapp em vez de startproject:

```bash
django-admin startapp products
```

</details>
</br>

<details>
<summary><strong> Criando uma tabela </strong></summary>

precisamos criar uma migration e executá-la:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

Lembre-se de executar os comandos acima dentro do diretório em que se encontra o arquivo manage.py.

O primeiro comando (makemigrations) cria um arquivo de migration - resumidamente, são as instruções para a criação da tabela no banco de dados. Ele já olha para o seu model e cria a migration pra você! Já o segundo comando (migrate) executa as migrações, ou seja, usa as instruções do arquivo de migration e cria a tabela no banco de dados.

</details>
</br>

<details>
<summary><strong> Inserindo dados no banco de dados via terminal </strong></summary>

O comando para acessar o terminal é:

```bash
python3 manage.py shell
```

Uma vez dentro do terminal, podemos importar o modelo que criamos:

```bash
from products.models import Product
```

A partir disso, podemos criar um novo objeto e salvá-lo no banco de dados:

```bash
moka = Product(name="Moka - 6 xícaras", price=199.99, amount=10, description="Cafeteira italiana, serve 6 xícaras, não elétrica")
moka.save()
```

</details>
</br>

## Django admin

O Django admin é uma ferramenta que permite a criação de um painel de administração para o projeto. Com ele, é possível visualizar, criar, editar e excluir objetos do banco de dados (o famoso CRUD), sem a necessidade de escrever código.

Lembra da rota '/admin' que você viu no arquivo urls.py? Ela é mais um exemplo dos recursos prontos para uso que o Django oferece, pois é ela que permite o acesso ao painel de administração do projeto.

Se você acessar agora mesmo localhost:8000/admin, verá que já existe um painel de administração criado. Ele exige, porém, um login, e não temos uma autenticação de admin configurada para o nosso projeto. Faremos essa configuração agora!

</details>
</br>

<details>
<summary><strong> Criando um superusuário </strong></summary>

A primeira coisa que devemos fazer é criar um superusuário para o projeto. Esse perfil terá permissões administrativas,ou seja, poderá acessar o painel de administração e realizar qualquer operação.

Para criar um superusuário, na raiz do projeto, execute o comando:

```bash
python3 manage.py createsuperuser
```

Será preciso informar um nome de usuário, e-mail e senha. Preencha os dados e, em seguida, acesse localhost:8000/admin e faça login com os dados de superusuário que você criou.

</details>
</br>

<details>
<summary><strong> Registrando o modelo </strong></summary>

Para que o Django admin funcione, é preciso registrar os modelos criados no arquivo admin.py, dentro da pasta do app. Fazer isso é bem simples: abra o arquivo ecommerce/products/admin.py e adicione o código:

```bash
from django.contrib import admin
from products.models import Product
from products.models import Customer # Modelo criado no exercício de fixação


admin.site.register(Product)
admin.site.register(Customer)
```

Já que estamos alterando este arquivo, que tal mudarmos também o cabeçalho do painel? Para isso, basta adicionar a linha no arquivo ecommerce/products/admin.py:

```bash
from django.contrib import admin
from products.models import Product


+ admin.site.site_header = "Trybe Products E-commerce"
admin.site.register(Product)
admin.site.register(Customer)
```

</details>
</br>

## Templates

<details>
<summary><strong> Configuração de Templates no Django </strong></summary>

Toda vez que um projeto Django é iniciado, um arquivo settings.py é criado dentro da pasta do projeto, e é dentro deste arquivo que é feita a configuração para indicar o mecanismo de template que será utilizado: Jinja2 ou o DTL.

Como o DTL é o mecanismo de template padrão do Django, não é necessário fazer nenhuma modificação para conseguir usá-lo. Contudo, caso no futuro você queira estudar o uso do Jinja2 como mecanismo de template, basta fazer a seguinte modificação no settings.py:

```bash
    ...
TEMPLATES = [
    {
-       'BACKEND': 'django.template.backends.django.DjangoTemplates',
+       'BACKEND': 'django.template.backends.jinja2.Jinja2',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
    ...
```

</details>
</br>

<details>
<summary><strong> Colocando o primeiro template para funcionar </strong></summary>

### Setup inicial

Para começar, crie o ambiente virtual que será utilizado e faça a instalação dos pacotes que serão utilizados:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install django
pip install Pillow # biblioteca para trabalhar com imagens
pip install mysqlclient # biblioteca para se comunicar com o MySQL
```

Em seguida, crie o projeto Django e a aplicação:

```bash
django-admin startproject event_manager .
django-admin startapp events
```

Faça a instalação da aplicação dentro do projeto no arquivo settings.py:

```bash
# event_manager/settings.py
...

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
+   'events',
]

...
```

Faça também a mudança para usar o MySQL como banco de dados:

```bash
# event_manager/settings.py
...

DATABASES = {
    'default': {
-       'ENGINE': 'django.db.backends.sqlite3',
+       'ENGINE': 'django.db.backends.mysql',
-       'NAME': BASE_DIR / 'db.sqlite3',
+       'NAME': 'event_manager_database',
+       'USER': 'root',
+       'PASSWORD': 'password',
+       'HOST': '127.0.0.1',
+       'PORT': '3306',
    }
}

...
```

Crie o arquivo para o script SQL dentro do diretório ./database:

```bash
mkdir database && cd database
touch 01_create_database.sql
```

Adicione o conteúdo do script para criação do banco de dados event_manager_database:

```bash
CREATE DATABASE IF NOT EXISTS event_manager_database;

USE event_manager_database;
```

Crie o Dockerfile na raiz do projeto:

```bash
FROM mysql:8.0.32

ENV MYSQL_ROOT_PASSWORD password
COPY ./database/01_create_database.sql /docker-entrypoint-initdb.d/data.sql01
```

Faça o build da imagem, basta rodar o comando dentro da pasta do projeto que contém o arquivo Dockerfile.

```bash
docker build -t event-manager-db .
```

Execute o container e o script de criação do banco copiado no Dockerfile:

```bash
Execute o container e o script de criação do banco copiado no Dockerfile:
```

Acesse o banco de dados pelo Workbench e verifique se ele foi criado corretamente.

Execute o comando migrate do Django:

```bash
python3 manage.py migrate
```

</details>
</br>

<details>
<summary><strong> Renderizando seu primeiro template </strong></summary>

Antes de começarmos, saiba que a configuração padrão do Django permite que você crie seus templates dentro de cada uma das aplicações do seu projeto, e assim faremos.

É possível alterar essa configuração para indicar diretórios específicos onde o Django deve procurar por templates. Por exemplo: na configuração abaixo, o Django irá buscar por templates dentro do diretório _templates_, que está na raiz do projeto e não mais dentro de cada uma das aplicações do projeto. Lembre-se que você não precisa fazer a alteração abaixo.

```bash
# event_manager/settings.py
+ import os

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
-       'DIRS': [],
+       'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

Agora sim, crie um novo diretório com nome templates dentro da aplicação events e, em seguida, crie o arquivo home.html dentro do novo diretório e inicie um arquivo HTML:

```bash
<!--events/templates/home.html-->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Primeiro Template</title>
</head>
<body>
    <h1> Meu primeiro template usando Django! </h1>
</body>
</html>
```

O próximo passo é implementar a view que irá fazer a renderização do template criado. Acesse o arquivo views.py dentro do app events e escreva a função que fará essa tarefa:

```bash
# events/views.py
from django.shortcuts import render


def index(request):
    return render(request, 'home.html')
```

Prontinho! A função acima usa o método render do Django para renderizar o template passado como segundo parâmetro home.html. O primeiro parâmetro, request, representa a requisição feita pela pessoa que usa a aplicação.

Mas agora você pode estar se perguntando: Como faço para invocar a função que foi implementada? 🤔

A resposta é: através das rotas da nossa aplicação. A função criada será vinculada a uma das rotas da aplicação e, em seguida, serão incluídas nas rotas da aplicação no projeto.

Crie o arquivo urls.py dentro da aplicação events e nele escreva o código abaixo:

```bash
# events/urls.py
from django.urls import path
from events.views import index


urlpatterns = [
    path("", index, name="home-page")
#   path("/rota-comentada", função-que-será-executada, name="nome-que-identifica-a-rota")
]
```

No código acima, uma lista de rotas (urlpatterns) foi definida e cada uma das rotas é definida através da função path, que recebe três parâmetros: o primeiro é o caminho para a rota em si ("" indica a raiz da aplicação https://localhost:8000/), o segundo é a função que será executada quando a rota for acessada e o terceiro é o nome que identifica essa rota.

Agora, será necessário incluir as rotas da aplicação no projeto principal. Para isso, acesse o arquivo urls.py do projeto e faça a seguinte alteração:

```bash
# event_manager/urls.py
  from django.contrib import admin
  from django.urls import path, include


  urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('events.urls'))
  ]
```

Com essas alterações você acabou de incluir as rotas da aplicação events no projeto event_manager, e fez isso usando o método include nativo do Django.

Acabou! 🎉🎉🎉 Execute o servidor e acesse a rota http://localhost:8000/ para ver o template criado sendo renderizado.

Relembrando 🧠: Para executar o servidor faça: python3 manage.py runserver no mesmo diretório em que se encontra o arquivo manage.py.
</details>
</br>

<details>
<summary><strong> Herança de templates</strong></summary>


O Django permite que não se crie toda a estrutura de HTML para cada um dos templates. A DTL (Django Template Language) permite que se crie um template base que contém a estrutura essencial do HTML e lacunas intencionais - com cada template filho preenchendo as lacunas com o próprio conteúdo. Esse mecanismo é chamado de Herança de templates. Como exemplo, relembre o template home.html que criamos:

```bash
<!-- events/templates/home.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Primeiro Template</title>
</head>
<body>
    <h1> Meu primeiro template usando Django! </h1>
</body>
</html>
```

Para ver a herança acontecendo na prática, copie todo o conteúdo desse arquivo e cole dentro de um novo arquivo HTML chamado base.html dentro do diretório events/templates.

Substitua, em seguida, o conteúdo da tag title (Primeiro Template) por {% block title %} {% endblock %}, além disso, também substitua a linha da tag h1 por {% block content %} {% endblock %}. Ao final dessas alterações o arquivo base.html fica assim:

```bash
<!-- events/templates/base.html -->
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} {% endblock %}</title>
</head>
<body>
    {% block content %} {% endblock %}
</body>
</html>
```

A sintaxe {% %} indica que está sendo usada uma Tag de template do DTL. Ela é a lacuna que mencionamos mais cedo - um template filho irá preenchê-la. Nesse caso, usamos a tag block. Existem muitas Tags de template já implementadas no DTL. Você pode conferir todas as tags nativas do DTL na documentação oficial.

Ao fazer essas alterações, foram criados blocos vazios que poderão ser preenchidos por aqueles templates que herdarem o arquivo base.html. Acima, criamos dois blocos - um chamado title e outro chamado content - para escrever o título da página que será exibida e para colocar todo o conteúdo HTML que se quer exibir, respectivamente.

Para usar a herança de template, faça o seguinte:

Vá no template filho e inclua no seu cabeçalho a seguinte sintaxe: {% extends 'base.html' %}, onde se usa a palavra reservada extends seguida de qual template se quer herdar.
Modifique o template filho, por exemplo o home.html, criando os blocos com os mesmos nomes daqueles criados no template herdado de acordo com a sintaxe abaixo.
Anota aí 📝: para que a herança aconteça é obrigatório que o {% extends 'nome-do-template.html' %} seja a primeira tag de template que aparece no arquivo.

```bash
<!-- events/templates/home.html -->
{% extends 'base.html' %}

{% block title %}
  Primeiro Template
{% endblock %}

{% block content %}
  <h1> Meu primeiro template usando Django! </h1>
{% endblock %}
```

Note que, ao invés de toda a estrutura base do HTML, você inclui as tags do template base e as preenche com o HTML que quiser. Ao rodar sua aplicação, verá que tudo continua funcionando, ou seja, a herança foi feita com sucesso! 👏

</details>
</br>

<details>
<summary><strong> Criando o model Event </strong></summary>

Antes de exibir a lista de eventos no template, é importante definir o modelo que será usado para representá-los. Eis ele abaixo:

```bash
# events/models.py
from django.db import models


class Event(models.Model):
    TYPE_CHOICES = (
        ('C', 'Conference'),
        ('S', 'Seminar'),
        ('W', 'Workshop'),
        ('O', 'Other'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    event_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    is_remote = models.BooleanField(default=False)
    image = models.ImageField(upload_to='events/img', blank=True)

    def __str__(self): # O método __str__ é sobrescrito para indicar como será a visualização do objeto
        return f'{self.title} - {self.date} - {self.location}' # Título do evento - Data - Local
```

A tabela event ao ser criada no banco terá 8 colunas, sendo elas:

id: inteiro e chave primária única pro evento (que não precisa ser explicitamente declarado no modelo);
title: texto com no máximo 200 caracteres;
description: texto sem limitação de caracteres;
date: data e hora do evento;
location: texto com no máximo 200 caracteres;
event_type: texto com no máximo 50 caracteres e que só pode assumir os valores C, S, W ou O (ao usar o parâmetro choices, o Django faz a validação se o valor inserido é um dos valores permitidos);
is_remote: booleano (True ou False) que indica se o evento é remoto ou não;
image: imagem que será salva na pasta {CAMINHO-DE-MÍDIA}/events/img (o caminho de mídia pode ser definido no arquivo settings.py)

Relembrando 🧠: quando há um campo imagem é preciso fazer a instalação do módulo Pillow. Para isso, basta executar o comando pip install Pillow no terminal. Relembrando 🧠: depois de definir o modelo que será usado, crie as migrations e logo depois migre-as para o banco. Para isso, execute python3 manage.py makemigrations e python3 manage.py migrate no terminal.

</details>
</br>

<details>
<summary><strong> Renderizando os eventos no template </strong></summary>

Toda função que renderiza um template usando o método render, do Django, é capaz também de fornecer um contexto para esse template. O termo contexto aqui se refere a um dicionário (dict), que pode ser construído dentro da função e passado para o template como terceiro parâmetro do método render.

Todas as chaves do contexto podem ser acessadas diretamente pelo template através da sintaxe {{ chave }}. Assim, o template fará a renderização do valor que estava associado à chave. Modifique a função index do arquivo events/views.py para que ela fique assim:

```bash
# events/views.py
from django.shortcuts import render


def index(request):
    context = {"company": "Trybe"}
    return render(request, 'home.html', context)
```

Modifique também seu template home.html para renderizar o valor da chave company do contexto:

```bash
<!-- events/templates/home.html -->
 {% extends 'base.html' %}

 {% block title %}
   Primeiro Template
 {% endblock %}

 {% block content %}
     <h1> Meu primeiro template usando Django! </h1>
     <h2> {{ company }} </h2>
 {% endblock %}
```

</details>
</br>

<details>
<summary><strong> Trabalhando com elementos do banco usando Python </strong></summary>

Você percebeu que o modelo Event herda de models.Model? Todas as classes que fazem essa mesma herança são usadas para representar tabelas do banco de dados. Pode não parecer importante, mas isso mostra o vínculo entre essa classe e a sua própria tabela no banco.

Além de representarem tabelas do banco, todas as classes que herdam de models.Model possuem um atributo chamado objects. Esse atributo permite a interação direta com o banco de dados usando a própria sintaxe do Python. Através desse atributo você pode criar novas entradas no banco, fazer consultas e até mesmo aplicar filtros em uma consulta. Já tivemos um gostinho disso no começo da seção.

Vamos ver na prática? 🤓

Execute o comando python3 manage.py shell no terminal, no mesmo diretório do arquivo manage.py. Esse comando abre o shell do Django já carregando suas configurações e permitindo usar o ORM do framework. Execute os comandos abaixo, linha a linha, para entender como podemos trabalhar com o banco de dados usando a sintaxe do Python:

```bash
from events.models import Event # importa o modelo Event

Event.objects.all() # retorna todos os eventos do banco. Se você não criou nenhum, o retorno será um QuerySet vazio

Event.objects.create(title='Conferência de Django', description='Evento massa sobre Django', date='2023-09-29 12:00:00-03:00', location='São Paulo', event_type='C', is_remote=False) # cria um novo evento no banco

Event.objects.all() # retorna todos os eventos do banco. Agora o retorno será um QuerySet com um evento a mais

Event.objects.create(title='Django Workshop', description='Workshop que acontece semestralmente sobre Django', date='2024-10-02 15:30:00-03:00', location='Web', event_type='W', is_remote=True) # cria outro evento no banco

Event.objects.filter(is_remote=True) # retorna apenas os eventos do banco que são remotos

Event.objects.filter(event_type='W') # retorna apenas os eventos do banco que são workshops

Event.objects.filter(event_type='C', is_remote=False) # retorna apenas os eventos do banco que são conferências e presenciais, simultaneamente

Event.objects.filter(date__year=2024) # retorna apenas os eventos do banco que acontecem em 2024

Event.objects.filter(date__range=['2023-01-01', '2024-12-31']) # retorna apenas os eventos do banco que acontecem entre 2023 e 2024
```

São muitas as possibilidades! 🤯

Uma segunda maneira de fazer a inserção de elementos no banco de dados é através da instanciação e depois uso do método save(). Além disso, quando um objeto do modelo é instanciado podemos também acessar o método delete() para removê-lo do banco. Veja só:

```bash
from events.models import Event # importa o modelo Event

Event.objects.all() # <QuerySet [<Event: Conferência de Django - 2023-09-29 15:00:00+00:00 - São Paulo>, <Event: Django Workshop - 2024-10-02 18:30:00+00:00 - Web>]>

evento_1 = Event(title='Django Devs', description='Pessoas fantásticas que usam Django se reunindo em um só lugar', date='2025-07-02 13:30:00-03:00', location='Web', event_type='W', is_remote=True) # instancia um novo evento

evento_1.save() # salva o evento no banco

evento_2 = Event(title='DjangoFest', description='Um festival um pouco menos legal que desenvolver com Django', date='2023-11-22 18:00:00-03:00', location='São Paulo', event_type='C', is_remote=False) # instancia outro evento

evento_2.save() # salva o evento no banco

Event.objects.all() # <QuerySet [<Event: Conferência de Django - 2023-09-29 15:00:00+00:00 - São Paulo>, <Event: Django Workshop - 2024-10-02 18:30:00+00:00 - Web>, <Event: Django Devs - 2025-07-02 16:30:00+00:00 - Web>, <Event: DjangoFest - 2023-11-22 21:00:00+00:00 - São Paulo>]>

evento_3 = Event(title='DJ ANGO', description='Conheça a mais nova sensação musical.', date='2027-06-19 20:00:00-03:00', location='São Paulo', event_type='C', is_remote=False) # instancia um evento idêntico ao anterior

evento_3.save() # salva o evento no banco

Event.objects.all() # <QuerySet [<Event: Conferência de Django - 2023-09-29 15:00:00+00:00 - São Paulo>, <Event: Django Workshop - 2024-10-02 18:30:00+00:00 - Web>, <Event: Django Devs - 2025-07-02 16:30:00+00:00 - Web>, <Event: DjangoFest - 2023-11-22 21:00:00+00:00 - São Paulo>, <Event: DJ ANGO - 2027-06-19 23:00:00+00:00 - São Paulo>]>

evento_3.delete() # remove o evento do banco

Event.objects.all() # <QuerySet [<Event: Conferência de Django - 2023-09-29 15:00:00+00:00 - São Paulo>, <Event: Django Workshop - 2024-10-02 18:30:00+00:00 - Web>, <Event: Django Devs - 2025-07-02 16:30:00+00:00 - Web>, <Event: DjangoFest - 2023-11-22 21:00:00+00:00 - São Paulo>]>
```

</details>
</br>

<details>
<summary><strong> Renderizando os eventos no template </strong></summary>

Agora sim! Finalmente será possível renderizar os eventos no template. Para isso, precisamos passar todos os eventos que estão no banco como contexto para o template. Modifique o contexto da função index no arquivo views.py para que exista uma chave events cujo valor será uma consulta com todos os eventos que estão cadastrados no banco de dados:

```bash
# events/views.py
from events.models import Event
from django.shortcuts import render


def index(request):
    context = {"company": "Trybe", "events": Event.objects.all()}
    return render(request, 'home.html', context)
```

Agora, adicione uma segunda tag h2 no template renderizando a chave events:

```bash
<!-- events/templates/home.html -->
{% extends 'base.html' %}

{% block title %}
  Primeiro Template
{% endblock %}

{% block content %}
    <h1> Meu primeiro template usando Django! </h1>
    <h2> {{ company }} </h2>
    <h2> {{ events }} </h2>
{% endblock %}
```

A visualização dos eventos ainda não está muito amigável, não é mesmo? 🙁 Isso acontece porque o retorno de Event.objects.all() é uma consulta (QuerySet), que pode ter 0, 1, 2, … n elementos. Para tornar essa visualização mais amigável é necessário iterar pelos elementos que existem na consulta e renderizar cada um deles individualmente.

A iteração pode ser feita usando a tag de template {% for %}, cuja sintaxe é muito semelhante à sintaxe do Python, com a diferença que você precisará indicar no template onde o for se encerra com a tag de _template_ {% endfor %}:

```bash
<!-- events/templates/home.html -->
{% extends 'base.html' %}

{% block title %}
  Primeiro Template
{% endblock %}

{% block content %}
     <h1> Meu primeiro template usando Django! </h1>
     <h2> {{ company }} </h2>
     {% for event in events %}
         <p> {{ event }} </p>
     {% endfor %}
{% endblock %}
```

A sintaxe acima permite que, dentro do template, seja feita uma iteração sobre cada um dos eventos presentes no contexto. Para cada elemento da iteração, é criada uma nova tag p renderizando aquele evento em específico.

Já imaginou o que aconteceria se a consulta não tivesse nenhum elemento? 🤔 A resposta é: nada! Em uma consulta vazia não haverá nenhum evento para renderizar e você deve concordar que isso também não é muito amigável! 😅

Para resolver isso vamos usar a tag de _template_ {% empty %} dentro do for, ela indicará o que queremos mostrar na tela caso não exista nenhum elemento na consulta que estamos fazendo:

```bash
<!-- events/templates/home.html -->
{% extends 'base.html' %}

{% block title %}
  Primeiro Template
{% endblock %}

{% block content %}
    <h1> Meu primeiro template usando Django! </h1>
    <h2> {{ company }} </h2>
    {% for event in events %}
       <p> {{ event }} </p>
    {% empty %}
       <p> Não existem eventos cadastrados </p>
    {% endfor %}
{% endblock %}
```

Agora sim! 🎉🎉🎉 Ainda da para melhorar um pouquinho a visualização dos eventos, mas espere um pouco para fazer isso. Antes, vamos à implementação da visualização dos detalhes de um evento específico. 🤓

</details>
</br>

<details>
<summary><strong> Criando o template de detalhes do evento </strong></summary>

Para conseguir criar o template de detalhes do evento, será necessário criar uma nova função no arquivo views.py. Essa função renderizará o novo template details.html que será criado dentro da pasta _templates_. Além disso, na função a ser implementada, é necessário passar à view o contexto com o evento específico que será renderizado no template.

Mas como o template saberá qual evento será renderizado? 😱 Resposta: Será recebido um parâmetro na função que permitirá o resgate do evento e sua renderização. No modelo Event, esse parâmetro é o id, chave primária do evento. Observe a implementação:

```bash
# events/views.py
from events.models import Event
from django.shortcuts import render
from django.shortcuts import get_object_or_404


def event_details(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'details.html', {'event': event})
```

```bash
<!-- events/templates/details.html -->
{% extends 'base.html' %}

{% block title %}
    {{ event.title }}
{% endblock %}


{% block content %}

    <h1>{{ event.title }}</h1>

    <p>{{ event.description }}</p>

    <p>{{ event.date|date }} - {{ event.location }}</p>

    {% if event.is_remote %}
        <p> Evento remoto </p>
    {% else %}
        <p> Evento presencial </p>
    {% endif %}

{% endblock %}
```

Na função event_details, o parâmetro event_id será recebido e utilizado para resgatar o evento específico que se quer renderizar. Esse resgate é feito com o uso da função get_object_or_404(), essa função recebe dois parâmetros: o primeiro é o modelo a ser resgatado e o segundo indica a busca a ser feita. No exemplo acima, é buscado por um Event cujo id é igual ao event_id recebido como parâmetro. Caso o evento não seja encontrado, será levantada uma exceção do tipo Http404.

Ao passar a chave event no contexto, é possível acessá-la dentro do template e usá-la para recuperar o evento alvo com todos os seus atributos. Esses atributos podem ser acessados dentro do template através da sintaxe {{ event.title }}, por exemplo. Assim, é possível montar um template genérico para a renderização de qualquer evento, desde que ele seja passado no contexto. 🤯

Perceba também que foi utilizada a sintaxe condicional com a Tag de Template {% if %} {% else %} e, assim como no {% for %}, é necessário indicar o fim da condição com {% endif %}.

Você deve ter notado o {{ event.date|date }} no template, né? A sintaxe para o uso de filtros de template é composta da variável à qual quer se aplicar o filtro seguida por um | e logo depois o nome do filtro. O filtro, nesse caso, é como uma máscara formatadora: ela pega a informação e ajusta a forma como ela será exibida. Nesse exemplo foi usado o filtro de data, para que a formatação da data seja no padrão DD de MMMMM de AAAA.

É possível, naturalmente, aplicar outras configurações para mostrar a data em outro formato. Além do filtro de data, existem outros filtros já implementados e que podem ser acessados em todos os templates como first, last, lower, upper, length, random, slugify, etc. Para saber mais sobre os filtros disponíveis, acesse a documentação oficial..

O código que foi apresentado ainda não funciona: falta vincular a função criada com uma rota específica, dentro do arquivo urls.py. Será nessa rota em que haverá a indicação de que o event_id será passado como parâmetro. Veja a implementação:

```bash
# events/urls.py
from django.urls import path
from events.views import index, event_details, about


urlpatterns = [
    path("", index, name="home-page"),
    path("about", about, name="about-page"),
    path("events/<int:event_id>", event_details, name="details-page"),
#   path("/rota-comentada", função-que-será-executada, name="nome-que-identifica-a-rota")
]
```

A rota events/<int:event_id> indica que a rota events/ será seguida de um número inteiro, que representa um event_id e que será passado como parâmetro para a função event_details. Vale lembrar que o nome da rota é importante para que seja possível acessá-la dentro do template.

</details>
</br>

<details>
<summary><strong>Conectando a página inicial com a página de detalhes</strong></summary>

A página de detalhes de um evento específico já funciona, acesse a rota events/<int:event_id> e veja! Entretanto, ainda não é possível acessá-la de maneira rápida e eficiente através da página inicial. Para adaptar a home.html , será necessário que você crie um link de redirecionamento para a página de detalhes de cada evento. Tarefa fácil ao usarmos a tag de template url que permite criar um link absoluto, veja:

```bash
<!-- events/templates/home.html -->
{% extends 'base.html' %}

 {% block title %}
   Primeiro Template
 {% endblock %}

 {% block content %}
     <h1> Meu primeiro template usando Django! </h1>
     <h2> {{ company }} </h2>
    {% for event in events %}
       <p> <a href="{% url 'details-page' event.id %}"> {{ event }} </a> </p>
    {% empty %}
        <p> Não existem eventos cadastrados </p>
    {% endfor %}
{% endblock %}
```

A tag de template {% url %} pode ser usada quando é necessário fazer a chamada de uma rota específica que já foi implementada e tem uma identificação no arquivo urls.py. No exemplo acima, a tag de template é usada para invocar a rota identificada como details-page, e, como essa rota necessita do id do evento como parâmetro, ele é passado logo em seguida com event.id. Assim, ao adicionar a tag a cujo atributo href aponta para a rota de detalhes já implementada, é feito o vínculo entre as rotas. Agora, ao executar a aplicação você deve ter algo como:

</details>
</br>

<details>
<summary><strong> Lidando com exceções </strong></summary>

O que será que acontece se uma pessoa tenta acessar uma página de evento que não existe? Tipo a página http://127.0.0.1:8000/events/99999 😱 A resposta para essa pergunta é: como durante a implementação a função get_object_or_404 foi usada, automaticamente, se não for possível resgatar o evento com id informado, será renderizada uma página padrão do Django indicando uma resposta 404, Not Found. Contudo, é possível personalizar, tratar essa exceção e exibir a página que desejar, veja só:

```bash
# events/views.py
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from events.models import Event


def event_details(request, event_id):
    try:
        event = get_object_or_404(Event, id=event_id)
        return render(request, 'details.html', {'event': event})
    except Http404:
        return render(request, '404.html')
```

Daí, basta implementar o template 404.html que deverá ser criado junto aos demais templates:

```bash
<!-- events/templates/404.html -->
{% extends 'base.html' %}

{% block title %}
    Página não encontrada
{% endblock %}

{% block content %}
    <h1> 404 - Página não encontrada </h1>
    <h2> Desculpe, mas o evento não foi encontrado </h2>
    <p><a href="{% url 'home-page' %}"> Volte a página inicial </a></p>
{% endblock %}
```

Agora, ao tentar acessar uma página de evento que não existe, a exceção Http404 levantada pela função get_object_or_404 será tratada pelo try/except e resulta na renderização da página 404.html. Na implementação da página foi usada a mesma sintaxe de herança de templates, e ao final do bloco content foi adicionado um link para a página inicial, usando novamente a tag de _template_ {% url %} vinculando assim uma rota previamente identificada no urls.py (home-page).

</details>
</br>

<details>
<summary><strong> Aprimorando os templates </strong></summary>

Pra finalizar a nossa aplicação, que tal acrescentarmos estilo, com CSS, às nossas páginas? Com isso feito, nossa aplicação já estará pronta pra ser usada!

Primeiro, vamos fazer uma alteração no nosso template home.html para facilitar a estilização da página. Vamos incluir um pouco mais de estrutura HTML para termos com o que trabalhar no CSS - além de incluir uma lógica para exibição de imagens dos eventos!

```bash
<!-- events/templates/home.html -->
 {% extends 'base.html' %}
 {% load static %}

 {% block title %}
   Primeiro Template
 {% endblock %}

 {% block content %}
     <h1> Eventos {{ company }} </h1>
    {% for event in events %}
        <a href="{% url 'details-page' event.id %}"> 
            <div>
              {% if event.image %}
                <img src="{% static event.image.url %}" alt="Imagem sobre o evento" height="50">
              {% endif %}
                <h3> {{ event.title }} </h3>
                <p> {{ event.date }} </p>
                <p> {{ event.location }} </p>
            </div>
        </a>
    {% empty %}
        <p> Não existem eventos cadastrados </p>
    {% endfor %}
 {% endblock %}
```

De olho na dica 👀: Se você tiver algum registro no banco de eventos que não possua imagem, a tag img não será renderizada em razão da condição imposta.

Use o painel admin para criar alguns eventos de maneira que você consiga fazer o upload de uma imagem que represente o evento. Para criar uma conta admin você pode executar python3 manage.py createsuperuser no mesmo diretório em que se encontra o arquivo manage.py. Além disso, também será necessário fazer o registro do modelo Event dentro do site, usando o arquivo admin.py:

```bash
from django.contrib import admin
from events.models import Event


admin.site.site_header = 'Event Manager Admin Panel'
admin.site.register(Event)
```

Mesmo adicionando um evento com imagem você ainda não será capaz de visualizar as imagens. Isso acontece porque ainda não fizemos a configuração de como vamos servir os arquivos estáticos do projeto.

</details>
</br>

<details>
<summary><strong> Arquivos estáticos </strong></summary>

O primeiro passo para fazer a configuração é instalar dois pacotes que ajudarão com essa tarefa:

```bash
pip install whitenoise # Serve os arquivos estáticos a partir de um diretório
pip install django-static-autocollect # Coleta os arquivos estáticos e os coloca em um diretório
```

Faça as modificações necessárias no arquivo settings.py:

```bash
# event_manager/settings.py
...

 INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'events',
+   'static_autocollect'
 ]

 MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
+   'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
 ]

 ...

+ MEDIA_URL = ''
+ MEDIA_ROOT = BASE_DIR / 'media'

 STATIC_URL = 'static/'
+ STATIC_ROOT = BASE_DIR / 'staticfiles'

+ STATICFILES_DIRS = [
+     str(BASE_DIR / 'media/'),
+ ]

+ STORAGE = {
+    "default": {
+        "BACKEND": "django.core.files.storage.FileSystemStorage",
+    },
+    "staticfiles": {
+        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
+    }
+ }

+ WHITE_NOISE_AUTOREFRESH = True
```

Com essas modificações estamos:

instalando o pacote static_autocollect no projeto;
adicionando o pacote whitenoise na lista de middlewares;
definindo o caminho relativo onde se encontra o diretório media em MEDIA_URL;
definindo o caminho absoluto em MEDIA_ROOT e que será usado como caminho base para o upload de imagens vindas das pessoas usuárias;
definindo o caminho absoluto em STATIC_ROOT e que será usado pelo whitenoise para servir os arquivos estáticos;
definindo uma lista de caminhos em STATICFILES_DIRS que serão usados pelo static_autocollect para coletar os arquivos estáticos e direcionar para STATIC_ROOT;
definindo o comportamento de armazenamento do whitenoise;
definindo que o whitenoise deve atualizar os arquivos estáticos automaticamente.
Use o comando python3 manage.py watch_static & python3 manage.py runserver para executar o servidor e o static_autocollect em paralelo. Agora, a próxima adição de registro que for feita já será refletida na página inicial.

De olho na dica 👀: A tag de template static serve para indicar o caminho relativo do arquivo estático e junto com os whitenoise e static_autocollect, possibilita servir os arquivos estáticos. Anota aí 📝: A metodologia mais comum para servir arquivos estáticos é separar e servi-los externamente, leia mais sobre isso.

Com um pouco de estilização, você pode deixar sua aplicação mais apresentável. Você pode usar CSS puro ou qualquer framework de CSS que desejar, fica à sua escolha e como se sentir mais confortável. A seguir temos um exemplo de estilização para a página inicial, ele foi feito usando o Tailwind CSS e contém exatamente as mesmas tags que foram apresentadas até então.

Você pode fazer o download dos templates estilizados: base.html e home.html. Nesse exemplo foi usado o CDN do Tailwind CSS, mas você poderia registrar o seu próprio arquivo CSS no template base.html.

</details>
</br>

## Formulários no Django

No Django, existe uma classe que permite que você consiga receber e validar dados de uma maneira rápida e prática. Essa é a classe Form, que está implementada no módulo django.forms.

Em resumo, um formulário pode ser criado para receber e validar dados que chegarão em uma requisição. Isso possibilita a criação ou atualização de registros no banco de dados de forma mais confiável.

<details>
<summary><strong> Criando um formulário </strong></summary>

Quando pensamos em criar um formulário, a primeira coisa a se fazer é definir qual será seu propósito. Como ele se encaixa na lógica da aplicação que estamos desenvolvendo para conseguirmos delimitar o que ele irá conter.

iniciaremos construindo um formulário cujo propósito é adicionar novas músicas ao banco.

Para isso, crie um arquivo forms.py dentro da aplicação playlists. É nesse arquivo que serão construídos os formulários da aplicação. Depois de criado, adicione o seguinte código:

```bash
# playlists/forms.py
from django import forms


class CreateMusicForm(forms.Form):
    name = forms.CharField(max_length=50)
    recorded_at = forms.DateField()
    length_in_seconds = forms.IntegerField()
```

Percebeu que os atributos do formulário que criamos têm praticamente a mesma sintaxe dos que foram criados no modelo Music?

Isso acontece porque para criar um novo registro na tabela music é obrigatório fornecer os três campos. Já para o modelo Playlist, por exemplo, os campos created_at e updated_at não precisam ser passados, então não precisamos desses campos:

```bash
# playlists/forms.py
from django import forms


class CreateMusicForm(forms.Form):
    name = forms.CharField(max_length=50)
    recorded_at = forms.DateField()
    length_in_seconds = forms.IntegerField()


+ class CreatePlaylistForm(forms.Form):
+     name = forms.CharField(max_length=50)
+     is_active = forms.BooleanField()
```

Uma grande vantagem de se usar um formulário é a maneira eficaz que ele proporciona a validação dos dados em cada campo.

Observe: o atributo name = forms.CharField(max_length=50) indica que o formulário deve ter uma entrada name do tipo String com no máximo 50 caracteres. Por outro lado, o atributo duration_in_seconds = forms.IntegerField() indica que o formulário deve ter uma entrada duration_in_seconds cujo valor correspondente deve ser do tipo inteiro.

</details>
</br>

<details>
<summary><strong> Formulários vinculados vs não vinculados </strong></summary>

Para o Django, formulários podem ser classificados como vinculados ou não vinculados.

Um formulário é considerado como não vinculado caso seja instanciado sem nenhum dado, caso contrário, ele é vinculado. A própria classe Form apresenta um atributo is_bound que indica se o formulário é vinculado ou não. Observe o exemplo abaixo:

```bash
from playlists.forms import CreatePlaylistForm


form = CreatePlaylistForm()
form.is_bound # retorna False

form = CreatePlaylistForm({"name":"Playlist de Estudo", "is_active": True})
form.is_bound # retorna True
```

De olho na dica 👀: qualquer dicionário passado como parâmetro já faz com que o formulário seja considerado como vinculado.

E afinal, qual a diferença? 🤔

Formulários vinculados podem validar os dados passados por parâmetro. Já formulários não vinculados não podem fazer isso. Veremos sobre isso a seguir!

</details>
</br>

</details>
</br>

<details>
<summary><strong> Validação de dados </strong></summary>

A classe Form implementa o método is_valid(), que retorna um booleano para informar se os dados do formulários são válidos ou não.

Além disso, a classe Form também implementa o atributo errors que retorna um dicionário com os erros de validação de cada campo do formulário. Veja o exemplo abaixo:

```bash
from playlists.forms import CreatePlaylistForm

form = CreatePlaylistForm({}) # formulário instanciado com um dicionário vazio
form.is_valid() # retorna False
form.errors # retorna {'name': ['Este campo é obrigatório.'], 'is_active': ['Este campo é obrigatório.']}

form_2 = CreatePlaylistForm({"name":"Essa playlist tem um nome com mais de cinquenta caracteres, o que você acha que vai acontecer?", "is_active": True})
form_2.is_valid() # retorna False
form_2.errors # retorna {'name': ['Certifique-se de que o valor tenha no máximo 50 caracteres (ele possui 94).']}

form_3 = CreatePlaylistForm({"name":"Playlist de Estudo", "is_active": True})
form_3.is_valid() # retorna True
form_3.errors # retorna {}

unbound_form = CreatePlaylistForm() #  formulário não vinculado
unbound_form.is_valid() #  retorna False
unbound_form.errors #  retorna {} Esse tipo de formulário não passa por validação
```

</details>
</br>

</details>
</br>

<details>
<summary><strong> Criando validações personalizadas </strong></summary>

É possível criar suas próprias funções de validação para os campos de um formulário, isso permite que você aplique a regra de negócio que quiser para validar um campo.

Para trazer o exemplo prático, vamos considerar que a duração de uma música, length_in_seconds, precisa ser um número inteiro entre 1 e 3600 segundos. A função de validação precisa levantar uma exceção ValidationError, que será implementada no módulo django.core.exceptions e que receberá como parâmetro a mensagem de erro que será exibida caso a validação falhe.

Crie um arquivo validators.py dentro da aplicação playlists e implemente uma função que faz a checagem se um número inteiro está entre 1 e 3600 segundos:

```bash
# playlists/validators.py

from django.core.exceptions import ValidationError


def validate_music_length(value):
    if value not in range(1, 3601):
        raise ValidationError(
            f"A duração da música deve ser um número"
            f" inteiro entre 1 e 3600 segundos. O valor "
            f"{value} não é válido."
        )

```

O próximo passo é indicar no campo do formulário que o dado recebido ali deve ser validado pela função criada, para além das validações padrão. Essa tarefa é feita por meio do parâmetro validators que recebe uma lista com todas as funções personalizadas para validação do campo. Veja abaixo:

```bash
# playlists/forms.py

from django import forms
+ from playlists.validators import validate_music_length


class CreateMusicForm(forms.Form):
    name = forms.CharField(max_length=50)
    recorded_at = forms.DateField()
+    length_in_seconds = forms.IntegerField(validators=[validate_music_length])
```

Agora, se você tentar criar uma música com uma duração menor que 1 ou maior que 3600 segundos, o formulário não será considerado válido e a mensagem de erro será exibida. Veja o exemplo abaixo:

Execute o código abaixo no terminal interativo do Django (python3 manage.py shell) ⚠️ Se você já estiver com um terminal interativo aberto, é necessário fechá-lo (exit()) e abrir um novo, pois, do contrário, as modificações feitas não serão consideradas.

```bash
from playlists.forms import CreateMusicForm


form = CreateMusicForm({"name":"The sound of silence", "recorded_at":"2023-07-05", "length_in_seconds":0}) # formulário instanciado com um dado inválido
form.is_valid() # retorna False
form.errors # retorna {'length_in_seconds': ['A duração da música deve ser um número inteiro entre 1 e 3600 segundos. O valor 0 não é válido.']}
```

De olho na dica 👀: o Django possui uma série de validações prontas para serem usadas, você pode conferir a lista com as validações na documentação oficial.

Além de indicar os validadores nos campos do formulário, também é possível indicar os validadores dentro do modelo da aplicação, utilizando o mesmo parâmetro (validators) na função que define cada campo.

Entretanto, é importante dizer que, mesmo que você indique os validadores no modelo, eles não serão executados automaticamente e ainda será possível criar registros com dados que não passam nas validações desejadas. Por isso, indicar os validadores no modelo pode parecer inútil, mas acredite, isso trará benefícios quando explorarmos outros tipos de formulários. 😉

Veja como fica o modelo com a validação:

```bash
# playlists/models.py

from django.db import models
+ from playlists.validators import validate_music_length

# ...

class Music(models.Model):
    name = models.CharField(max_length=50)
    recorded_at = models.DateField()
+    length_in_seconds = models.IntegerField(validators=[validate_music_length])

    def __str__(self):
        return self.name
```

Relembrando 🧠: como foi feita uma modificação no modelo, lembre-se de criar as migrações e migrá-las para o banco de dados. Para isso, execute os comando: python3 manage.py makemigrationse python3 manage.py migrate.

</details>
</br>

</details>
</br>

## Renderizando formulários em templates

Relembrando 🧠: para criar um novo registro no banco, você pode usar o método .create() do atributo objects, do modelo em questão.

<details>
<summary><strong> Novo registro a partir de um formulário </strong></summary>

Uma vez que você já possui um formulário que tem dados válidos, é preciso repassar esses dados para o modelo e, assim, criar o novo registro no banco. Para isso, depois de usar o método is_valid() para checar a integridade dos dados passados, você pode usar o atributo cleaned_data para que um dicionário com todos os dados sejam retornados para você. Esses dados, agora já validados, podem ser usados para criar um novo registro no banco.

O passo a passo abaixo demonstra como é possível fazer isso e pode ser executado no terminal interativo do Django:

```bash
from playlists.forms import CreateMusicForm
from playlists.models import Music

form = CreateMusicForm({"name":"Be brave, Dev", "recorded_at":"2023-06-05", "length_in_seconds":180})

if form.is_valid():
    data = form.cleaned_data # data será igual à {"name":"Be brave, Dev", "recorded_at":"2023-06-05", "length_in_seconds":180}
    Music.objects.create(**data) # criando um novo registro no banco com os dados do formulário
    # Music.objects.create(**data) é o mesmo que Music.objects.create(name="Be brave, Dev", recorded_at="2023-06-05", length_in_seconds=180)
```

Você pode apertar a tecla enter duas vezes para sair do escopo da condição (if) que acabamos de criar. 😉

Anota aí 📝: A sintaxe **data é do Python e é uma desestruturação para passar cada um dos pares chave e valor, individualmente, como parâmetros.

Prontinho! Conseguimos conectar os conhecimentos sobre criação de registros no banco de dados e formulários. 🤩 O próximo passo agora é receber os dados direto da requisição e, a partir deles, criar o novo registro no banco. Vamos lá?

</details>
</br>

</details>
</br>

<details>
<summary><strong> Formulários e templates </strong></summary>

Você já sabe que podemos renderizar variáveis passadas como contexto para um template. Vamos explorar esse recurso?

Crie o diretório templates dentro da aplicação playlists e nele crie os dois primeiros templates base.html e music.html. Implemente a estrutura para herança de templates e, no arquivo music.html, renderize a variável form dentro do bloco content.

```bash
<!-- playlists/templates/base.html -->

<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %} {% endblock %}</title>
</head>
<body>
    {% block content %} {% endblock %}    
</body>
</html>
```

```bash
<!-- playlists/templates/music.html -->

{% extends 'base.html' %}

{% block title %}
    Formulário para Nova Música
{% endblock %}

{% block content %}
    {{form}}
{% endblock %}
```

Implemente a primeira função no arquivo views.py com nome de music que irá renderizar music.html. Passe no contexto uma instância do formulário CreateMusicForm como valor da chave form.

```bash
# playlists/views.py

from django.shortcuts import render
from playlists.forms import CreateMusicForm


def music(request):
    form = CreateMusicForm()
    context = {"form": form}
    return render(request, "music.html", context)
```

Crie o arquivo urls.py, dentro da aplicação playlists. Nele, configure a rota para a função create_music que você acabou de criar.

```bash
# playlists/urls.py

from django.urls import path
from playlists.views import music


urlpatterns = [
    path("musics/", music, name="musics-page"),
]
```

Por fim, inclua a rota da aplicação no arquivo urls.py do projeto.

```bash
# playlist_manager/urls.py

from django.contrib import admin
+ from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
+     path("", include("playlists.urls"))
]
```

Execute a aplicação (python3 manage.py runserver) e veja como o formulário é renderizado na tela. 😱

A instância do formulário é convertida para um conjunto de tags HTML que renderizam o formulário criado por você. Você pode alterar a forma como esse formulário é renderizado por meio de alguns atributos com layouts diferentes. Usaremos aqui o as_p:

```bash
<!-- playlists/templates/music.html -->

{% extends 'base.html' %}

{% block title %}
    Formulário para Nova Música
{% endblock %}

{% block content %}
+     {{form.as_p}}
{% endblock %}
```

Experimente trocar o as_p por as_div e as_ul, inspecione o conteúdo HTML ao usar cada um e veja a diferença entre eles!

Você deve ter notado, também, que embora o formulário esteja lá, não temos nenhum botão para enviar os dados. Veremos, após o exercício, como incluí-l.o 😉

</details>
</br>

<details>
<summary><strong> Personalizando o formulário </strong></summary>

O formulário renderizado no template ainda não está dentro do que é esperado. Os nomes que designam cada um dos campos ainda estão em inglês e, além disso, é necessário modificar os campos que são renderizados. Por exemplo, recorded_at, que representa uma data, está sendo renderizado como um campo de texto.

Essas configurações podem ser feitas diretamente no formulário, no momento de se definir a classe. Podemos usar o parâmetro labels para indicar qual deverá ser o nome de cada um dos campos. Ainda, podemos usar o parâmetro initial para sugerir um dado inicial caso faça sentido para aquele campo. Veja como fica a implementação do formulário CreateMusicForm ao usarmos esses parâmetros:

```bash
# playlists/forms.py

from django import forms
from playlists.validators import validate_music_length, validate_name


class CreateMusicForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        label="Nome da música",
    )
    recorded_at = forms.DateField(
        label="Data de gravação",
        initial="2023-07-06",
    )
    length_in_seconds = forms.IntegerField(
        validators=[validate_music_length],
        label="Duração em segundos",
    )
```

De olho na dica 👀: também é possível usar o parâmetro help_text para indicar uma frase de auxílio no preenchimento do campo. Experimente!

Colocar um valor inicial pode ajudar no preenchimento do campo, mas isso não necessariamente melhora a experiência da pessoa usuária. Contudo, é possível melhorar essa experiência modificando a aparência dos campos do formulário com um widget.

Um widget nada mais é do que uma representação HTML mais elaborada de um campo input. Felizmente, o Django tem diversos widgets já implementados e prontos para serem usados. Além disso, ele também permite que você crie seus próprios widgets! 🤯

Para usar um widget, basta passá-lo como parâmetro ao definir o campo, assim como é feito para o parâmetro label.

Para fazer as melhores escolhas, é necessário conhecer os widgets disponíveis e você pode ver a lista completa de widgets nativos do Django na documentação oficial. Aqui, usaremos o DateInput():

```bash
# playlists/forms.py

from django import forms
from playlists.validators import validate_music_length, validate_name


class CreateMusicForm(forms.Form):
    name = forms.CharField(
        max_length=50,
        validators=[validate_name],
        label="Nome da música",
    )
    recorded_at = forms.DateField(
        label="Data de gravação",
+         widget=forms.DateInput(attrs={"type": "date"}),
        initial="2023-07-06",
    )
    length_in_seconds = forms.IntegerField(
        validators=[validate_music_length],
        label="Duração em segundos",
    )
```

De olho na dica 👀: o parâmetro attrs passado para o widget é usado para atribuir um conjunto chave: valor à tag que está sendo inserida no template. Nesse caso, definimos o tipo do input como data type: date, mas poderíamos, adicionalmente, definir uma classe: class: inputDate.

Execute o servidor antes e depois da adição do novo widget. Essa implementação diminui a probabilidade de bugs relacionados à entrada de dados do tipo data, que precisam ser digitados em um formato específico. Além disso, ainda houve uma melhora na experiência de quem usa o formulário.

</details>
</br>

<details>
<summary><strong> Enviando dados do template para a view </strong></summary>

Se você inspecionar o conteúdo HTML do formulário que está renderizado no template, verá que, apesar de chamarmos de formulário, não há tag form alguma. Isso é um problema, pois queremos enviar os dados inseridos para algum local, então vamos dar um jeito nisso!

O primeiro passo é justamente envolver o formulário em uma tag form, indicando o método HTTP e ação que será realizada quando o formulário for submetido.

Além disso, duas outras coisas são necessárias: adicionar uma tag input capaz de submeter o formulário (type: submit) e adicionar {% csrf_token %} logo após a tag form.

A tag de template {% csrf_token %} é uma estratégia de segurança do framework contra Cross-site Request Forgery. Se quiser ler mais sobre esse tipo de ataque, visite esse site aqui.

```bash
<!-- playlists/templates/music.html -->

{% extends 'base.html' %}

{% block title %}
    Formulário para Nova Música
{% endblock %}

{% block content %}
+    <form method="post" action="">
+        {% csrf_token %}
        {{form.as_p}}
+        <input type="submit" value="Submeter formulário">
+    </form>
{% endblock %}
```

Neste ponto, você já deve ser capaz de submeter o formulário, contudo, esses dados não estão indo para lugar algum. É preciso indicar qual função da camada view receberá os dados submetidos pela requisição (request).

O parâmetro request possui atributos e métodos. Todos os dados que são submetidos por meio de formulários podem ser visualizados no atributo POST, na forma de um dicionário. Entretanto, se os dados forem enviados no body da requisição, eles podem ser acessados no atributo body na forma de bytes. Além disso, também é possível identificar o método HTTP utilizado por meio do atributo method. Logo mais veremos isso na nossa aplicação!

Adicione a tag de template {% url %} para invocar a rota musics-page no template music.html:

```bash
<!-- playlists/templates/music.html -->

{% extends 'base.html' %}

{% block title %}
    Formulário para Nova Música
{% endblock %}

{% block content %}
+    <form method="post" action="{% url 'musics-page' %}">
        {% csrf_token %}
        {{form.as_p}}
        <input type="submit" value="Submeter formulário">
    </form>
{% endblock %}
```

Agora, ao submeter o formulário, você está enviando os dados submetidos para a função music que, por sua vez, renderiza novamente o template music.html.

Para conseguir visualizar no terminal os dados que estão sendo submetidos e o body da requisição, adicione os prints abaixo à função music e refaça a submissão do formulário:

```bash
# playlists/views.py

from django.shortcuts import render
from playlists.forms import CreateMusicForm


def music(request):
+    print(request.POST)
+    print(request.body)
+    print(request.method)
    form = CreateMusicForm()
    context = {"form": form}
    return render(request, "music.html", context)
```

Parabéns, você conseguiu passar dados de um template para uma função da camada view! 🎉 O próximo passo é usar esse formulário para validar os dados enviados e, em seguida, criar um novo registro no banco!

De olho na dica 👀: sempre que você quiser inspecionar métodos e atributos de uma variável, você pode usar o método dir, nativo do Python. Acrescente print(dir(request)) aos prints da função e veja o que é mostrado no terminal ao submeter o formulário.

</details>
</br>

<details>
<summary><strong> Criando o novo registro </strong></summary>

Iremos implementar uma nova função chamada index, que recebe no contexto todos os objetos Music. Também iremos renderizar um novo template home.html, no qual serão colocados na tela todos os objetos criados e um link de redirecionamento para a função music.

A implementação de ambos pode ser observada abaixo:

```bash
# playlists/views.py

# ...
from playlists.models import Music


def index(request):
    context = {"musics": Music.objects.all()}
    return render(request, "home.html", context)

# ...
```

```bash
<!-- playlists/templates/home.html -->

{% extends 'base.html' %}

{% block title %}
    Home Page
{% endblock %}

{% block content %}
    {% for music in musics %}
        <p>{{music}}</p>
    {% endfor %}

    <a href="{% url 'musics-page' %}">Criar nova música</a>
{% endblock %}
```

Registre a função index no arquivo urls.py:

```bash
# playlists/urls.py

from django.urls import path
+ from playlists.views import music, singer, index


urlpatterns = [
+    path("", index, name="home-page"),
    path("musics/", music, name="musics-page"),
    path("singers/", singer, name="singers-page"),
]
```

Para finalizar o processo de criação, basta implementar a lógica da instanciação e validação de um formulário e, se os dados forem válidos, adicionar o novo registro no banco e redirecionar para o template inicial home.html. Usaremos o método redirect e passaremos como parâmetro a identificação da rota desejada: home-page.

É preciso lembrar que esse processo completo só deve acontecer caso o método HTTP da requisição seja POST. Vale lembrar também que o próprio formulário passado como contexto para o template é capaz de ligar com erros, caso existam.

Observe a implementação da função music:

```bash
# playlists/views.py

from django.shortcuts import render, redirect
from playlists.forms import CreateMusicForm, CreateSingerForm
from playlists.models import Music


def music(request):
    form = CreateMusicForm()

    if request.method == "POST":
        form = CreateMusicForm(request.POST)

        if form.is_valid():
            Music.objects.create(**form.cleaned_data)
            return redirect("home-page")

    context = {"form": form}

    return render(request, "music.html", context)
```

Agora sim! Você conseguiu criar um novo registro no banco de dados por meio de um formulário! 🎉

Execute o servidor e veja funcionando! python3 manage.py runserver

</details>
</br>

## Formulários de modelos (ModelForm)

Pode até ser que você já tivesse se questionado quanto à isso, mas imagine: você tem um modelo que tem 10 atributos necessários para a criação de um novo registro, você precisaria fazer a implementação de cada um desses atributos no modelo e depois “repetir” todos os atributos no formulário de criação. Isso não parece muito eficiente, e se fossem 20, 30 ou 50 atributos? 😵‍💫

O ModelForm tem em sua implementação uma maneira para lidar com esse tipo de problema que foi mencionado. Ele é um formulário que usa como base um modelo já criado, no qual você pode explicitar os campos que deseja que apareçam para a pessoa usuária.

<details>
<summary><strong> ModelForm na prática </strong></summary>

Usando como base o projeto construído até aqui, você vai implementar o primeiro ModelForm que será usado para a criação de novos registros de Music. Comece uma nova classe com o nome CreateMusicModelForm e faça a herança de form.ModelForm. Além disso, para fazer esse formulário funcionar corretamente, será necessário implementar a classe Meta dentro da classe CreateMusicModelForm (Isso mesmo, uma classe dentro da outra 🤯) e nessa segunda classe implementar os atributos: model, fields, labels e widgets.

* O atributo model é usado para indicar o modelo que será usado como base, e recebe o nome da classe do modelo.
* O atributo fields pode receber a string __all__ ou uma lista com os nomes dos atributos do modelo que você deseja que apareçam no formulário, sendo que a primeira opção faz com que todos os atributos apareçam.
* O atributo labels recebe um dicionário onde as chaves são os atributos do modelo e os valores são suas respectivas labels personalizadas.
* O atributo widgets recebe um dicionário onde as chaves são os atributos do modelo e os valores são os respectivos widgets que serão visualizados. É no campo de widgets que você pode personalizar um valor inicial para o atributo do modelo.

Veja a implementação como fica:

```bash
# playlists/forms.py
from playlists.models import Music

# ...

class CreateMusicModelForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = "__all__"
        labels = {
            "name": "Nome da música",
            "recorded_at": "Data de gravação",
            "length_in_seconds": "Duração em segundos",
        }
        widgets = {
            "recorded_at": forms.DateInput(
                attrs={"type": "date", "value": "2023-07-06"}
            )
        }
```

Com o novo formulário implementado basta fazer a substituição na função create_music dentro do arquivo views.py.

```bash
# playlists/views.py
def create_music(request):
    # form = CreateMusicForm()
    form = CreateMusicModelForm()

    if request.method == "POST":
        # form = CreateMusicForm(request.POST)
        form = CreateMusicModelForm(request.POST)

        if form.is_valid():
            Music.objects.create(**form.cleaned_data)
            return redirect("home-page")

    context = {"form": form}

    return render(request, "index.html", context)
```

Você verá que o formulário já estará funcionando 🤩, inclusive, as validações. Se lembra de quando foi falado que seria útil indicar validações para o campo no próprio modelo? Pois é, esse momento é agora. O ModelForm já estrutura seus campos inserindo as validações. Tente criar uma música com duração maior que 3600 e verá a mensagem na tela.

Agora sim! O ModelForm está idêntico ao Form construído anteriormente. É importante retomar o ponto que não há implementação certa ou errada nesse cenário, tudo depende da aplicação que será construída. Por exemplo, se os nomes padrões fossem bons o suficiente para a aplicação, seguir com a implementação da ModelForm seria mais interessante e pouparia algumas linhas de código na aplicação.

</details>
</br>

## Relacionamento de Modelos

<details>
<summary><strong> Relacionamento 1 para N </strong></summary>

Refletindo sobre os modelos acima, é possível perceber que essa relação se encaixa bem com os modelos Singer <1:N> Music, dado que uma mesma pessoa cantora pode ter várias músicas, certo?.

Ao se analisar a implementação dos modelos acima, se nota que nenhum dos campos descritos é uma chave primária. Quando não criamos esse campo explicitamente o Django, automaticamente, cria uma nova coluna para cada modelo, chamada id, que será a chave primária, caso algum dos campos seja designado como chave primária (primary_key = True), o Django não criará a coluna id.

Para criar o relacionamento entre os modelos Singer e Music, será utilizado o campo models.ForeignKey no modelo Music, onde será implementado que uma música pode possuir apenas uma pessoa cantora. Dessa forma, se N músicas diferentes referenciam a mesma pessoa cantora, podemos notar a relação Singer <1:N> Music.

No campo models.ForeignKey será necessário passar o modelo a ser referenciado e logo em seguida outros dois parâmetros: on_delete, que define o que acontecerá com os registros que estão associados ao registro que está sendo excluído e related_name, que será um atributo do modelo referenciado para permitir o acesso no sentido inverso do relacionamento.

Além disso, se existirem registros no banco de dados, será necessário definir um valor padrão para que as colunas adicionais sejam preenchidas. Algumas estratégias que podem ser usadas:

* Criar um objeto que representará o valor padrão e passar seu id como valor padrão. (Usaremos essa aqui)
* Permitir que a coluna seja nula e, posteriormente, preencher os valores.
* Ou caso ainda esteja em fase de desenvolvimento, apagar o banco e as migrações e criar tudo novamente.

Crie um objeto do tipo Singer usando o terminal interativo do Django python3 manage.py shell:

```bash
from playlists.models import Singer


default = Singer.objects.create(name="Pessoa desconhecida")  # Retorna o objeto criado <Singer: Pessoa desconhecida>

default.id # Retorna o id do objeto criado, 2, por exemplo
```

Agora, veja como fica a classe Music com o relacionamento:

```bash
# playlists/models.py
from django.db import models
from playlists.validators import validate_music_length,


class Music(models.Model):
    name = models.CharField(max_length=50)
    recorded_at = models.DateField()
    length_in_seconds = models.IntegerField(validators=[validate_music_length])
    singer = models.ForeignKey(
        Singer,
        on_delete=models.CASCADE,
        related_name="musics",
        default=2, # Se não houver o objeto com esse id em seu banco você terá um erro ao criar um objeto Music
    )

    def __str__(self):
        return self.name
```

De olho na dica 👀: Para o parâmetro on_delete existem algumas opções de valor já implementadas pelo Django dentro de models. Você encontra essas opções na documentação oficial.

Com a implementação acima, o modelo Music referencia o modelo Singer. Já que modificamos o modelo é necessário aplicar as migrações para o banco python3 manage.py makemigrations e python3 manage.py migrate.

Na prática, será criada uma coluna adicional na tabela music com o nome singer_id que armazenará a chave primária do registro da tabela singer que está sendo referenciado, independentemente se essa chave primária é um id ou não. Além disso, foi usada a configuração on_delete=models.CASCADE, indicando que, caso o registro da tabela singer seja excluído, todos os registros da tabela music que possuem o singer_id igual ao id do registro excluído, também serão excluídos.

Um ponto importante a ser observado é que o atributo singer da classe Music precisa receber um objeto do tipo Singer para ser criado e não um id ou qualquer outra chave primária. O ORM do Django se encarrega da tarefa de, a partir do objeto Singer, escrever a chave primária no banco de dados e, ao fazer o resgate do banco, resgatar o objeto singer a partir do id registrado no banco.

Na prática, através de um objeto Music podemos acessar o objeto Singer através do atributo singer. Já através de um objeto Singer, podemos acessar todos os objetos Music associados à ele através do atributo musics, definido em related_name do relacionamento e, em seguida, usando o método all().

Observe o exemplo abaixo do relacionamento 1:N para entender melhor essa relação:

```bash
from playlists.models import Music, Singer

corey = Singer.objects.create(name="Corey Taylor") # cria objeto Singer com id = 1 e salva em corey

music_1 = Music.objects.create(name="Snuff", recorded_at="2008-06-17", length_in_seconds=270, singer=corey) # cria objeto Music com id = 1 e salva em music_1

music_2 = Music.objects.create(name="Through Glass", recorded_at="2006-07-01", length_in_seconds=240, singer=corey) # cria objeto Music com id = 2 e salva em music_2

music_1.singer # retorna o objeto Singer associado ao objeto Music music_1
# saída: <Singer: Corey Taylor>

music_2.singer # retorna o objeto Singer associado ao objeto Music music_2
# saída: <Singer: Corey Taylor>

corey.musics.all() # retorna todos os objetos Music associados ao objeto Singer corey
# saída: <QuerySet [<Music: Snuff>, <Music: Through Glass>]>
```

</details>
</br>

<details>
<summary><strong> Relacionamento N para N </strong></summary>

O relacionamento N para N representa uma relação onde um registro de uma tabela pode estar associado a vários registros de outra tabela e vice-versa. No caso aqui, podemos fazer transpor essa relação para os modelos Music e Playlist, dado que uma música pode estar em várias playlists e uma playlist pode ter várias músicas.

Para implementar esse relacionamento no Django, será usado o campo models.ManyToManyField, que recebe o modelo a ser referenciado e o parâmetro related_name, com o mesmo intuito anterior, ser possível fazer o acesso reverso ao modelo que está sendo referenciado.

```bash
# playlists/models.py
class Playlist(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    musics = models.ManyToManyField("Music", related_name="playlists")

    def __str__(self):
        return self.name
```

O único motivo pelo qual o modelo Music se encontra entre aspas, como se fosse uma string, no parâmetro models.ManyToManyField é que, no momento da criação do modelo Playlist, o modelo Music ainda não foi declarado. Dessa forma, o Django busca pelo modelo Music apenas depois que todos os modelos forem declarados.

No Django, quando um relacionamento N:N é criado, o atributo responsável por esse relacionamento se torna uma espécie de set que pode receber objetos do tipo do modelo referenciado. Assim, é possível adicionar, usando o método add(), ou remover, usando o método remove() objetos do atributo de relacionamento.

Uma vez que uma música é adicionada à uma playlist, é preciso salvar novamente a playlist para que as atualizações sejam refletidas no banco de dados. Por essa razão, pode-se implementar métodos que encapsulam essa lógica e facilitam o gerenciamento dos objetos. Observe:

```bash
# playlists/models.py
from django.db import models


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    musics = models.ManyToManyField("Music", related_name="playlists")

    def add_music(self, music):
        self.musics.add(music)
        self.save()
    
    def remove_music(self, music):
        self.musics.remove(music)
        self.save()

    def __str__(self):
        return self.name
```

Assim, todos os objetos do tipo Playlist serão capazes de usar os métodos add_music() e remove_music() que facilitam a adição e remoção de músicas de uma playlist. Para conseguir visualizar todas as músicas de uma playlist, basta acessar o atributo musics do objeto Playlist e, em seguida, usar o método all(). Já, se o intuito é visualizar todas as playlists que uma música está associada, basta acessar o atributo playlists do objeto Music, também definido em related_name do relacionamento e, em seguida, usar o método all().

Novamente, foram feitas alterações nos modelos e para que sejam observadas no banco, é preciso criar e executar as migrações python3 manage.py makemigrations e python3 manage.py migrate. Observe o exemplo abaixo do relacionamento N:N para entender melhor essa relação:

```bash
from playlists.models import Music, Playlist

music_1 = Music.objects.get(id=1) # retorna objeto Music com id = 1 e salva em music_1

music_2 = Music.objects.get(id=2) # cria objeto Music com id = 2 e salva em music_2

playlist_1 = Playlist.objects.create(name="Codando na Paz", is_active=True) # cria objeto Playlist com id = 1 e salva em playlist_1

playlist_2 = Playlist.objects.create(name="Bora Treinar", is_active=True) # cria objeto Playlist com id = 2 e salva em playlist_2

playlist_1.musics.all() # retorna todos os objetos Music associados ao objeto Playlist
# saída: <QuerySet []>

playlist_2.musics.all() # retorna todos os objetos Music associados ao objeto Playlist
# saída: <QuerySet []>

playlist_1.add_music(music_1) # adiciona objeto Music music_1 ao objeto Playlist

playlist_1.musics.all() # retorna todos os objetos Music associados ao objeto Playlist
# saída: <QuerySet [<Music: Snuff>]>

playlist_2.add_music(music_1) # adiciona objeto Music music_1 ao objeto Playlist

playlist_2.musics.all() # retorna todos os objetos Music associados ao objeto Playlist
# saída: <QuerySet [<Music: Snuff>]>

playlist_2.add_music(music_2) # adiciona objeto Music music_2 ao objeto Playlist

playlist_2.musics.all() # retorna todos os objetos Music associados ao objeto Playlist
# saída: <QuerySet [<Music: Snuff>, <Music: Through Glass>]>

music_1.playlists.all() # retorna todos os objetos Playlist associados ao objeto Music
# saída: <QuerySet [<Playlist: Codando na Paz>, <Playlist: Bora Treinar>]>

music_2.playlists.all() # retorna todos os objetos Playlist associados ao objeto Music
# saída: <QuerySet [<Playlist: Bora Treinar>]>
```


</details>
</br>

<details>
<summary><strong> Como ficam os formulários agora? </strong></summary>

Na última implementação realizada dos formulários, foi utilizada a classe ModelForm que, automaticamente, cria os campos do formulário com base nos campos do modelo. Você chegou a visualizar como ficou o formulário depois que as alterações de relacionamento foram feitas?

O nome que designa o novo campo ainda não foi personalizado mas, sem alterar nada da implementação do formulário, temos um novo campo funcional que já resgata todos os objetos do tipo Singer do banco e coloca na lista de seleção.

Caso houvesse a intenção de mostrar apenas alguns dos objetos Singer, seria possível personalizar o widget do campo singers para que ele fosse um form.Select passando o parâmetro choices com o valor de uma lista de tuplas, onde cada tupla contém, respectivamente, o valor a ser submetido no formulário e o valor exibido para a pessoa usuária. Observe:

```bash
# music/forms.py
class CreateMusicModelForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].label = "Nome da música"
        self.fields["recorded_at"].label = "Data de gravação"
        self.fields["recorded_at"].widget = forms.DateInput(
                attrs={"type": "date"})
        self.fields["recorded_at"].initial = "2023-07-06"
        self.fields["length_in_seconds"].label = "Duração em segundos"
        self.fields["singer"].label = "Artista"
        self.fields["singer"].widget = forms.Select(
            choices=[
                (singer.id, singer.name)
                for singer in Singer.objects.filter(name__contains="a")
            ]
        )
```

Com a modificação acima, o campo singer do formulário passa a exibir os nomes dos objetos Singer que possuem a letra “a” no nome, entretanto, ao submeter o formulário não será o nome do objeto que será passado adiante, mas sim o seu id.

Execute o servidor e veja as alterações feitas em funcionamento: python3 manage.py runserver e acesse localhost:8000/musics.

</details>
</br>

# DRF - Django Rest Framework

<details>
<summary><strong> Instalações </strong></summary>

```bash
pip install django djangorestframework
```

A documentação oficial do DRF recomenda a instalação de algumas outras dependências para serem utilizadas no desenvolvimento de APIs com esse framework. Hoje, utilizaremos duas delas: o markdown e o django-filter, além do mysqlclient que nos permitirá utilizar o MySQL como banco de dados. Para instalá-los, basta executar:

```bash
pip install markdown django-filter mysqlclient
```

* Criação do projeto e app, instalação do app no settings
* Configuração do banco de dados
* Migrações
* Criação do super usuário e fazer o login

</details>
</br>

## Primeiros passos com DRF - Models

O ponto de partida será incluir o rest-framework no projeto. Uma vez que ele já está instalado no ambiente virtual, basta adicioná-lo à variável INSTALLED_APPS, no arquivo playlistify.settings.py do projeto:

```bash
# ...
"core",
+ "rest_framework",
```

A partir disso, o Django já reconhece o DRF e podemos começar a utilizá-lo.

<details>
<summary><strong> Models </strong></summary>

Em seguida, é preciso que os modelos da API sejam definidos. Como dito anteriormente, nossa API será construída para o gerenciamento de playlists e por isso, utilizaremos os mesmos três modelos do dia sobre Formulários com Django, que são: Singer, Playlist e Music, de forma que o arquivo core/models.py ficará como a seguir:

```bash
from django.db import models


class Singer(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Music(models.Model):
    name = models.CharField(max_length=50)
    recorded_at = models.DateField()
    length_in_seconds = models.IntegerField()
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name="musics")

    def __str__(self):
        return self.name


class Playlist(models.Model):
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    musics = models.ManyToManyField("Music", related_name="playlists")

    def add_music(self, music):
        self.musics.add(music)
        self.save()

    def remove_music(self, music):
        self.musics.remove(music)
        self.save()

    def __str__(self):
        return self.name
```

Relembrando 🧠: O relacionamento entre os modelos Singer e Music é <1:N>, pois uma música pode pertencer a apenas uma pessoa artista, mas cada artista pode ter várias músicas. Enquanto isso, o relacionamento entre Musice Playlist é de <N:N>, dado que uma música pode estar em várias playlists e uma playlist pode ter várias músicas.

Com os modelos definidos, podemos parar o servidor com o atalho ctrl+ c e logo em seguida criar as migrations e aplicá-las ao banco de dados com os comandos:

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

</details>
</br>

<details>
<summary><strong> Registrando os models no admin </strong></summary>

Ainda não registramos os modelos no arquivo core/admin.py. É isso que faremos agora:

```bash
from django.contrib import admin
from .models import Singer, Music, Playlist

admin.site.register(Singer)
admin.site.register(Music)
admin.site.register(Playlist)
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