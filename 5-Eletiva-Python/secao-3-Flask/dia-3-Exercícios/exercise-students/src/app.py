from flask import Flask, render_template, request, redirect, url_for
from os import environ
from waitress import serve

app = Flask(__name__)

students = [
  {"name": "Ana", "register": 1234},
  {"name": "Bruno", "register": 5678},
  {"name": "Carlos", "register": 2345},
  {"name": "Daniela", "register": 6789},
  {"name": "Eduardo", "register": 3456},
]


@app.route("/")
@app.route("/alunos")
def get_all_students():
   return render_template('students.html', students=students)


@app.route("/alunos/adicionar", methods=["GET", "POST"])
def add_student():
  if request.method == "POST":
    name = request.form.get('name')
    register = request.form.get('register')

    students.append({
        "name": name,
        "register": int(register)
    })

    return redirect('/')
  
  return render_template('add_student.html')


@app.route("/alunos/editar/<int:index>", methods=["GET", "POST"])
def update_student(index):
  if request.method == "POST":
    students[index]["name"] = request.form.get('name')
    students[index]["register"] = request.form.get('register')
    return redirect('/')
  
  return render_template('update_student.html', student=students[index], aluno_index=index)


def start_server(host: str = '0.0.0.0', port: int = 8000):
  if environ.get("FLASK_ENV") == "dev":
      app.run(debug=True, host=host, port=port)
  else:
     serve(app, host=host, port=port)


if __name__ == "__main__":
   start_server()