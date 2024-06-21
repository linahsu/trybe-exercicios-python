from flask import Flask, render_template, request, redirect
from os import environ
from waitress import serve
from models.movie import Movie
from controllers.movies_controller import MoviesController

app = Flask(__name__)


@app.route("/", methods=["GET"])
def get_all_movies():
  movies = Movie.find_movie_by_title()
  return render_template('index.html', movies=movies)

@app.route("/search/<int:index>", methods=["POST"])
def search_movies(index):
  pass

@app.route("/<int:index>", methods=["GET"])
def find_one_movie(index):
  movie = MoviesController.find_movie_by_title(index)
  return render_template('movie.html', movie=movie)


def start_server(port=9000):
  if environ.get('FLASK_ENV') == 'dev':
    app.run(debug=True, port=port)
  else:
    serve(app, port=port)

if __name__ == "__main__":
  start_server()