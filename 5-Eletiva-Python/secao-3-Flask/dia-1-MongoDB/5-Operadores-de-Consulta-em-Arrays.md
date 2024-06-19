## Operadores de Consulta em Arrays

O MongoDB nos oferece um operador, que verifica a presença de valores dentro de um array, este operador é o $all

### $all

Funciona como operador "and"

##### db.places.find({ amenities: { $all: ["Stove", "Refrigerator"] } })

Atenção, com o comando abaixo, o comportamento é diferente do que usar o operador $all!!!

##### db.places.find({ amenities: ["Garagem", "jacuzzi", "Armários", "piscina"] })

- A query acima retornará somente os documentos em que o array amenities seja exatamente igual ao passado como parâmetro no filtro, ou seja, contenha apenas esses elementos e na mesma ordem!
- Já a query utilizando o operador $all, analisará o mesmo array, independentemente da existência de outros valores ou da ordem em que os elementos estejam.

### $elemMatch

Funciona como operador "or"

Ele seleciona todos os documentos que satisfaçam pelo menos um critério. Ou seja, com esse operador você pode especificar várias queries para um mesmo array.

##### db.places.find( {amenities: { $elemnMatch: { $in: ['TV', 'Stove'] } } }, {})