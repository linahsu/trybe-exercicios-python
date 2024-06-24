class Book:
  def __init__(self, title: str, author: str, year: str):
    self.title = title
    self.author = author
    self.year = year

  def to_dict(self):
    return {
      "title": self.title,
      "author": self.author,
      "year": self.year,
    }
  
book_harry = Book(
  "Harry Potter e a Pedra Filosofal", 
  "J.K.Rowling", 
  "1999",
)
