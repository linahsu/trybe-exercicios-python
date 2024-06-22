from flask import jsonify
from models.movie import Movie

class MoviesController:
  def find_movie_by_title(self, title: str = None):
    query = { "titulo": title } if title else None
    
    movies = Movie.find_movie_by_title(query)

    return [movie.to_dict() for movie in movies]
    

  def find_movie_by_id(self, id):
    movie = Movie.find_movie_by_id(id)

    if not movie:
      return jsonify({ "error": "Filme não encontrado" }), 404
    
    return movie.to_dict()