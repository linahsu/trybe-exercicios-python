## Método Delete

- Método deleteOne(): Para deletar apenas um documento;
- Método deleteMany(): Para deletar vários documentos.

### deleteOne()

##### db.places.deleteOne({ _id: 11 })

Atenção: Esse método sempre remove apenas um documento que bata com o critério passado! Caso você não passe filtros na query, ela irá remover o primeiro registro da coleção.

### deleteMany()

A query abaixo remove todos os documentos de imóveis que não tenham sido verificados, ou seja, que contenham o valor do campo host.host_identity_verified como false.

##### db.places.deleteMany({ "host.host_identity_verified": { $eq: false } })

Atenção: O comando abaixo remove todos os documentos da coleção:

##### db.places.deleteMany({})