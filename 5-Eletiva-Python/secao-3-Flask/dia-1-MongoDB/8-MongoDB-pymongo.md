## MongoDB

### pymongo

Agora que temos nossos dados, precisamos armazenar esta informação. Para isto utilizaremos o MongoDB que, como já estudamos, é um banco de dados de documentos, que armazena dados em formato JSON (BSON). Precisaremos de uma biblioteca para nos comunicarmos com o sistema de gerenciamento do banco de dados, e a mais popular e robusta é a pymongo. Podemos instalá-la com o comando:

⚠️Lembre-se que para testar o código abaixo você deve criar um ambiente virtual e instalar o pymongo conforme é ensinado abaixo.

##### python3 -m venv .venv && source .venv/bin/activate
##### python3 -m pip install pymongo

Após a instalação vamos ver como podemos realizar a escrita e leitura neste banco de dados. O primeiro passo é criar uma conexão com o banco de dados e isto pode ser feito da seguinte maneira:

⚠️ Lembre-se que o MongoDB deve estar preparado para ser acessado do “outro lado” dessa operação!.

##### Exemplo no arquivo pymongo.py