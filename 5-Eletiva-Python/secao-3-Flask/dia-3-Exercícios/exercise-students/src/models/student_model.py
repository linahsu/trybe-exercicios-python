from dataclasses import dataclass, asdict
from pymongo.collection import Collection
from .db import db


@dataclass
class Student:
  name: str
  register: int

  def to_dict(self):
    return asdict(self)

@dataclass
class StoredStudent(Student):
  _id: str

  def __post_init__(self):
    self._id = str(self._id)

class StudentsList:
  _collection: Collection = db["students"]

  @classmethod
  def get_all_students(cls):
    return [StoredStudent(**student) for student in cls._collection.find()]
  
  @classmethod
  def find_one_student(cls, query = {}):
    student = cls._collection.find_one(query)
    return student if student else None

  @classmethod
  def add_student(cls, student: dict):
    cls._collection.insert_one(student)

  @classmethod
  def update_student(cls, query, student: dict):
    cls._collection.find_one_and_update(
      query,
      { "$set": student }
    )

  @classmethod
  def remove_student(cls, id: str):
    cls._collection.delete_one({ "_id": id })
