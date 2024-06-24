from flask import Flask
from os import environ
from waitress import serve
from controllers.home_controller import home_controller
from controllers.book_controller import book_controller

app = Flask(__name__)

app.template_folder = "views/templates"

app.register_blueprint(home_controller, url_prefix="/")
app.register_blueprint(book_controller, url_prefix="/book")

def start_server(host = "0.0.0.0", port = 8000):
  if environ.get("FLASK_ENV") == "dev":
    return app.run(debug=True, host=host, port=port)
  else:
    serve(app, host=host, port=port)

if __name__ == "__main__":
  start_server()