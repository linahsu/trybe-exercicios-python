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


</details>
</br>

<details>
<summary><strong> Configuração de Templates no Django </strong></summary>

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