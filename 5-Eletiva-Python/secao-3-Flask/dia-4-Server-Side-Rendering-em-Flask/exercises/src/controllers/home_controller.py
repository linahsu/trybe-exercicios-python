from flask import Blueprint, render_template

home_controller = Blueprint("home_controller", __name__)

@home_controller.route("/", methods=["GET"])
def index():
  welcome_message = "Seja bem vindo!"
  return render_template("index.html", welcome_message=welcome_message)