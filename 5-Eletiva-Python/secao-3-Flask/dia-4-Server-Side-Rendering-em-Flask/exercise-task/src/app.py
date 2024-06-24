from flask import Flask
from os import environ
from waitress import serve

app = Flask(__name__)

app.template_folder = "views/templates"

def start_server(host = "0.0.0.0", port = 8000):
  if environ.get("FLASK_ENV") == "dev":
    return app.run(debug=True, host=host, port=port)
  else:
    serve(app, host=host, port=port)

if __name__ == "__main__":
  start_server()