from flask import Blueprint, jsonify, request, render_template, redirect
from models.student_model import Student, StoredStudent, StudentsList

bp = Blueprint("students", __name__)


@bp.route("/")
@bp.route("/alunos")
def get_all_students():
   students = StudentsList.get_all_students()
   return render_template('students.html', students=students)


@bp.route("/alunos/adicionar", methods=["GET", "POST"])
def add_student():
  if request.method == "POST":
    name = request.form.get('name')
    register = request.form.get('register')

    StudentsList.add_student({
        "name": name,
        "register": int(register)
    })

    return redirect('/')
  
  return render_template('add_student.html')


@bp.route("/alunos/editar/<int:index>", methods=["GET", "POST"])
def update_student(index):
  student = StudentsList.find_one_student({ "register": int(index) })
  if request.method == "POST":
    name = request.form.get("name")
    register = request.form.get("register")
    student_to_update = { "name": name, "register": int(register) }
    StudentsList.update_student({ "register": int(index) }, student_to_update)

    return redirect('/')
  
  return render_template('update_student.html', student=student, student_index=index)


@bp.route("/alunos/excluir/<int:index>", methods=["GET", "POST"])
def remove_student(index):
  student = StudentsList.find_one_student({ "register": int(index) })
  if request.method == "GET":
     return render_template('remove_student.html', student=student, student_index=index)
  
  StudentsList.remove_student(student)
  return redirect('/')