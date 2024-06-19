from pymongo import MongoClient

# Em posse da conexão podemos acessar um banco de dados e posteriormente uma
# coleção:
# Por padrão o host é localhost e porta 27017
# Estes valores podem ser modificados passando uma URI
# client = MongoClient("mongodb://localhost:27017/")
client = MongoClient()

# o banco de dados catalogue será criado se não existir
db = client.catalogue

# a coleção books será criada se não existir
students = db.books

# Para adicionarmos documentos à nossa coleção utilizamos o método insert_one:
book = {
    "title": "A Light in the Attic",
}
document_id = students.insert_one(book).inserted_id
print(document_id)
# Quando um documento é inserido, um _id único é gerado e retornado

# Também podemos fazer inserção de múltiplos documentos
documents = [
    {
        "title": "A Light in the Attic",
    },
    {
        "title": "Tipping the Velvet",
    },
    {
        "title": "Soumission",
    },
]
students.insert_many(documents)

# Buscas podem ser feitas utilizando os métodos find ou find_one:
# busca um documento da coleção, sem filtros
print(students.find_one())
# busca utilizando filtros
for book in students.find({"title": {"$regex": "t"}}):
    print(book["title"])

client.close()  # fecha a conexão com o banco de dados

# O nosso cliente é um gerenciador de contexto (with), logo podemos utilizá-lo
# como tal, evitando problemas com o fechamento da conexão com o banco de
# dados:

with MongoClient() as client:
    db = client.catalogue
    for book in db.books.find({"title": {"$regex": "t"}}):
        print(book["title"])
