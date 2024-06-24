import os
from pymongo import MongoClient

client = MongoClient(os.environ.get("MONGO_URL", "mongodb://localhost:27017"))

# db = client.db_project
# Caso não exista a varíavel de ambiente "TEST_DATABASE"(banco de dados para teste), 
# o db usa p "db_project" (banco de dados da produção)
db = client[os.getenv("TEST_DATABASE", "db_project")]

# pip install pytest-env

# pyproject.toml
# + env = [
# +    "TEST_DATABASE=test_db_project",
# + ]
