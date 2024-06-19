## Utilizando MongoDB com Docker

### Utilizando imagem Docker MongoDB a qual irá inicializar um servidor MongoDB

##### docker run --name mongodb_v6 -d -p 27017:27017 mongo:6.0

O comando acima inicializa um container chamado mongodb_v6, com a imagem do MongoDB em sua versão 6 e vincula a porta 27017 do seu computador local com a mesma porta do container.

### Executando o shell do MongoDB no Docker

Para manipular os banco de dados, coleções e documentos no MongoDB, utilizaremos uma ferramenta de linha de comando chamada mongosh (Mongo Shell).

Para termos acesso a um shell com o mongosh no container Docker que acabamos de iniciar, vamos executar o comando a seguir:

##### docker exec -it mongodb_v6 mongosh

### Importando uma base de dados para o MongoDB

Para realizar a cópia de um arquivo do computador local para o container, podemos usar o comando docker cp. Então, após realizar o download do arquivo JSON, em uma nova aba ou janela do terminal, vá até o diretório onde foi salvo o arquivo JSON após o download e execute o seguinte comando:

##### docker cp trybnb.json mongodb_v6:/tmp/trybnb.json

Bacana, agora temos o arquivo JSON no container! Podemos então realizar o procedimento de carregar o arquivo JSON para o MongoDB. Logo, vamos utilizar uma ferramenta chamada mongoimport.

A ferramenta mongoimport importa conteúdo de um arquivo .JSON, .CSV ou .TSV criados pela ferramenta utilitária mongoexport.

Vamos utilizar o comando docker exec para executar o comando mongoimport dentro do container a partir do nosso computador local. 
Agora podemos realizar a importação do arquivo JSON executando o comando a seguir:

##### docker exec mongodb_v6 mongoimport -d trybnb -c places --file /tmp/trybnb.json --jsonArray

Nesse ponto, já podemos manipular os documentos importados através do mongosh. Execute os seguinte comandos para listar os documentos cadastrados:

##### use trybnb
##### db.places.find()

- Na primeira linha, usamos o comando use trybnb, para dizer ao mongosh se conectar ao banco de dados trybnb;
- Na segunda linha, usamos o comando db.places.find(), para listar todos os documentos presentes na coleção places.
