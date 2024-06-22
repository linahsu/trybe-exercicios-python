from pymongo.collection import Collection
from .db import db
from bson.objectid import ObjectId

class Movie:
  _collection: Collection = db["movies"]

  def __init__(self, data):
    self.data = data

  @classmethod
  def find_movie_by_title(cls, query = {}):
    movies = cls._collection.find(query)
    return [cls(movie) for movie in movies]
  
  @classmethod
  def find_movie_by_id(cls, id):
    movie = cls._collection.find_one({ "_id": ObjectId(id) })
    return cls(movie) if movie else None
  
  def to_dict(self):
    return {
      "titulo": self.data["titulo"],
      "ano": self.data["ano"],
      "diretor": self.data["diretor"],
      "genero": self.data["genero"],
      "poster": self.data["poster"],
      "_id": self.data["_id"],
    }