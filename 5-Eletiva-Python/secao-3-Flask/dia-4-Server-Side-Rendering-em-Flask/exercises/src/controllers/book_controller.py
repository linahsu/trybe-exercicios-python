from flask import Blueprint, render_template
from models.book_model import book_harry

book_controller = Blueprint("book_controller", __name__)

@book_controller.route("/", methods=["GET"])
def book():
  return render_template("book.html", book=book_harry.to_dict())