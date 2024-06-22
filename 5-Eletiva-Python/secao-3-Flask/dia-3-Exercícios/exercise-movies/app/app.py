from flask import Flask, render_template, request, redirect
from os import environ
from waitress import serve
from controllers.movies_controller import MoviesController

app = Flask(__name__)
movie_controller = MoviesController()


@app.route("/", methods=["GET", "POST"])
def get_all_movies():
  if request.method == "POST":
    title = request.form["title"]
    movies = movie_controller.find_movie_by_title(title)
  else:
    movies = movie_controller.find_movie_by_title()
  return render_template('index.html', movies=movies)


@app.route("/<id>")
def get_one_movie(id):
  movie = movie_controller.find_movie_by_id(id)
  return render_template('movie.html', movie=movie)


def start_server(host='0.0.0.0', port=8000):
  if environ.get("FLASK_ENV") == "dev":
    app.run(debug=True, host=host, port=port)
  else:
    serve(app, host=host, port=port)

if __name__ == "__main__":
  start_server()