from flask import Flask
from os import environ
from waitress import serve

app = Flask(__name__)


def start_server(host: str = '0.0.0.0', port: int = 8000):
  if environ.get("FLASK_ENV") == "dev":
      app.run(debug=True, host=host, port=port)
  else:
     serve(app, host=host, port=port)


if __name__ == "__main__":
   start_server()