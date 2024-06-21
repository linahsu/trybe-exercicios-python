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
    pass

  @classmethod
  def add_student(cls, student: Student):
    pass

  @classmethod
  def update_student(cls, id: str):
    pass

  @classmethod
  def remove_student(cls, id: str):
    pass
