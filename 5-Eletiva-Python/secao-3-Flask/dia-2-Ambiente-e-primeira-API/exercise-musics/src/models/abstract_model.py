from pymongo.collection import ReturnDocument, Collection

class AbstractModel:
  _collection: Collection = None

  def __init__(self, data: dict) -> None:
    self.data = data

  def save(self):
    result = self._collection.insert_one(self.data)
    self.data = self._collection.find_one(
      { "_id": result.inserted_id }
    )
    return self.data
  
  @classmethod
  def find(cls, query: dict = {}):
    data = cls._collection.find(query)
    return [cls(d) for d in data]
  
  @classmethod
  def find_one(cls, query: dict = {}):
    data = cls._collection.find_one(query)
    return cls(data) if data else None    