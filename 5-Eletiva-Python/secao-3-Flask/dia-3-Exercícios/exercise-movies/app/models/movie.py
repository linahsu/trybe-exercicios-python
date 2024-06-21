from pymongo.collection import Collection
from .db import db

class Movie:
  _connection: Collection = db["movies"]

  def __init__(self, data):
    self.data = data

  def find_movie_by_title(self, title: str = None):
    if not title:
      return [movie for movie in self._connection.find()]
    
    movie = self._connection.find_one({ "titulo": title })
    return movie if movie else None
  
  def find_movie_by_id(self, id: str):
    movie = self._connection.find_one({ "_id": id })
    return movie if movie else None
  
  def to_dict(self):
    return {
      "titulo": self.data["titulo"],
      "ano": self.data["ano"],
      "diretor": self.data["diretor"],
      "genero": self.data["genero"],
      "poster": self.data["poster"],
      "_id": self.data["_id"],
    }