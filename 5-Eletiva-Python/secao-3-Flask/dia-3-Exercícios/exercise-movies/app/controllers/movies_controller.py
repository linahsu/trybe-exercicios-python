from flask import jsonify
from models.movie import Movie

class MoviesController:
  def find_movie_by_title(title: str = None):
    return Movie.find_movie_by_title(title)
    

  def find_movie_by_id(id: str):
    movie = Movie.find_movie_by_id(id)

    if not movie:
      return jsonify({ "error": "Filme não encontrado" }), 404
    
    return movie