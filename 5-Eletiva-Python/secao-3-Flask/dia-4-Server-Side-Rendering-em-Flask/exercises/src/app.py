from flask import Flask
from os import environ
from waitress import serve
from controllers.home_controller import home_controller
from controllers.book_controller import book_controller
from controllers.movies_controller import movies_controller
from controllers.product_controller import product_controller

app = Flask(__name__)

app.template_folder = "views/templates"

app.register_blueprint(home_controller, url_prefix="/")
app.register_blueprint(book_controller, url_prefix="/book")
app.register_blueprint(movies_controller, url_prefix="/movies")
app.register_blueprint(product_controller, url_prefix="/products")

def start_server(host = "0.0.0.0", port = 8000):
  if environ.get("FLASK_ENV") == "dev":
    return app.run(debug=True, host=host, port=port)
  else:
    serve(app, host=host, port=port)

if __name__ == "__main__":
  start_server()