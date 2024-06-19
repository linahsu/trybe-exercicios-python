## Método Update

### Método updateOne(): Para alterar apenas um valor;

Fazendo o update:
##### deb.places.updateOne({ _id: 101 }, { $set: { name: "...", description: "..." } })

Criando uma chave nova:
##### deb.places.updateOne({ _id: 101 }, { $set: { isFree: ... } })

Deletando uma chave:
##### deb.places.updateOne({ _id: 101 }, { $unset: { name: "...", description: "..." } })

### Método updateMany(): Para alterar vários valores.

Fazendo o update:
##### deb.places.updateMany({ _id: { $gte: 100 } }, { $set: { name: "...", description: "..." } })

Criando uma chave nova:
##### deb.places.updateMany({ _id: { $gte: 100 } }, { $set: { isFree: ... } })

Deletando uma chave:
##### deb.places.updateMany({ _id: { $gte: 100 } }, { $unset: { name: "...", description: "..." } })