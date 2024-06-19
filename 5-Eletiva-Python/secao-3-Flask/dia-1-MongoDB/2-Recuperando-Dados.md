## Recuperando Dados

### Realizando uma busca por todos os documentos

Antes de tudo, entraremos no terminal do mongosh e vamos nos conectar ao banco de dados trybnb executando o seguinte comando:

##### use trybnb

Caso desejasse mudar de banco, bastaria digitar use <nome_do_banco> para efetivar tal ação.

A primeira pergunta que podemos realizar ao MongoDB sobre os dados do banco trybnb é: “quais são os imóveis cadastrados no trybnb?”. Essa pergunta é o equivalente a realizar uma busca por todos os documentos cadastrados na coleção places. Logo, podemos escrever o seguinte comando no mongosh:

##### db.places.find()

Em um banco de dados relacional, o correspondente do método db.places.find() seria o SELECT * FROM places.

### Realizando a contagem de documentos

##### db.places.countDocuments()

O método countDocuments() realiza a contagem de documentos de uma determinada coleção (no nosso caso, da coleção places). Após sua execução, será exibido o valor 12 que é a quantidade de documentos cadastrados na coleção.

### Recuperando documentos baseado em um critério

Também é possível recuperar documentos baseado em algum critério de seleção, similar à cláusula WHERE dos banco de dados relacionais.

Não foi comentado antes, mas o método find() pode receber dois parâmetros:

- Parâmetro query;
- Parâmetro projection.

Ambos os parâmetros são opcionais e, quando não informados, o método find() realiza a busca de todos os documentos (como mostrado anteriormente).

### Parâmetro query

Suponha que queremos saber qual imóvel tem o _id igual a 7 (uma pergunta a ser respondida pelo banco de dados). Podemos obter essa resposta adicionando o parâmetro query ao método find() da seguinte forma:

##### db.places.find({ '_id': 7 })

Em um banco de dados relacional, o correspondente do método db.places.find({ '_id': 7 }) seria o SELECT * FROM places WHERE _id = 7.

O MongoDB utiliza o campo _id como identificador dos documentos, funcionando de forma similar a coluna id (chave primária) dos bancos de dados relacionais. Agora vamos supor que gostaríamos de saber quais imóveis estão localizados no Brasil, ou seja, uma nova pergunta a ser respondida pelos dados do banco trybnb. Existe um campo chamado country_code cujo valor é o código do país do imóvel. Este campo está dentro de um objeto chamado address, que também é um campo.

Neste caso, como existe um aninhamento de campos (o campo country_code é filho do campo address) teremos que utilizar um campo composto (em inglês também pode ser chamado de dotNotation) para filtrar os dados. Em outras palavras, temos que executar o seguinte comando no terminal do mongosh:

##### db.places.find({ 'address.country_code': 'BR' })

Ao executar o comando acima, receberemos como resultado um conjunto de documentos cujo o valor de address.country_code é igual a BR. Em um banco de dados relacional seria o equivalente realizar uma consulta SELECT com um JOIN, dado que, pela terceira forma normal, places seria uma tabela e address seria outra tabela.

Para finalizar, quantos imóveis temos disponíveis para locação no Brasil? Temos uma nova pergunta para ser respondida! Diferente do que vimos no início da lição, onde usamos o método db.places.countDocuments() para contar o total de documentos da coleção, agora queremos contar quantos documentos o método find() retornou após utilizar o parâmetro query.

Basicamente, basta escrevermos a consulta do mesmo modo que já fizemos e adicionar o método count() ao final, da seguinte forma:

##### db.places.find({ 'address.country_code': 'BR' }).count()

### Parâmetro projection

O parâmetro projection permite especificar quais campos devem ou não ser retornados em uma consulta utilizando o método find().

Para deixar isso mais nítido, vamos trabalhar com a consulta que recupera o imóvel cujo o campo _id seja igual a 7, ou seja:

##### db.places.find({ '_id': 7 })

Ao executar o comando acima, é exibido o documento cujo o valor do campo _id é igual a 7, conforme já foi visto anteriormente. Mas vamos supor que apenas queremos exibir o nome do imóvel e omitir os demais campos.

Para alcançar este objetivo, utilizaremos o parâmetro projection para definir quais campos devem ser exibidos na resposta da consulta. Para isso, devemos executar o método find() com o seguinte conteúdo:

##### db.places.find({ '_id': 7 }, { 'name': true })

Como resposta, será exibido o campo _id e o campo name (nome do imóvel)!

A projection é um objeto que pode conter um ou mais campos com valor true (ou false como veremos mais adiante), onde apenas os campos especificados na projection como true serão exibidos na resposta da consulta.

Agora vamos supor que queremos, além de exibir o nome do imóvel, exibir o endereço do imóvel cujo o campo _id seja igual a 7. Sabemos que existe uma campo address que contém os dados do endereço do imóvel. Logo, o comando para atender o esperado seria:

##### db.places.find({ '_id': 7 }, { 'name': true, 'address': true })

Quando a projeção contêm campos cujo os valores são iguais a true, temos uma projeção de inclusão, ou seja, na resposta são incluídos os campos definidos na projeção e as demais são ignoradas. Podemos também, utilizando o parâmetro projection, realizar o inverso, ou seja, ao pesquisar um documento, quais campos deseja-se omitir. Para isso, na projection atribuímos o valor false ao campo que queremos omitir.

Por exemplo, se escrevermos o seguinte comando no mongosh:

##### db.places.find({ '_id': 7 }, { 'address': false, 'host': false })

Quando a projeção contêm campos cujos valores são iguais a false, temos uma projeção de exclusão, ou seja, na resposta são exibidos todos os campos exceto os campos definidos na projeção.

### Ordenando uma resposta

Caso você deseje que esses dados retornem ordenados baseados no valor de uma chave, podemos utilizar o método sort(). Observe o exemplo abaixo:

##### db.places.find().sort({'_id': 1})

Para realizar essa ordenação de forma decrescente, basta mudarmos o valor 1 para -1, ou seja:

##### db.places.find().sort({'_id': -1})

