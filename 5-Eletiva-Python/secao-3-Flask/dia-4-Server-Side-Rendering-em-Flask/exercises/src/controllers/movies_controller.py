from flask import Blueprint, render_template

movies_controller = Blueprint("movies_controller", __name__)

movies = [
  {"title": "The Shawshank Redemption", "published_year": "1994"},
  {"title": "The Godfather", "published_year": "1972"},
  {"title": "The Dark Knight", "published_year": "2008"},
  {"title": "Pulp Fiction", "published_year": "1994"},
  {"title": "Forrest Gump", "published_year": "1994"},
]

@movies_controller.route("/", methods=["GET"])
def movies_index():
  return render_template("movies.html", movies=movies)
