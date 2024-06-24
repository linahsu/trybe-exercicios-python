from flask import Blueprint, render_template, request
from models.task_model import Task

task_controller = Blueprint("task_controller", __name__)

tasks = [
  Task(1, "lavar roupas"),
  Task(2, "beber água"),
  Task(3, "fazer almoço"),
]

@task_controller.route("/", methods=["GET", "POST"])
def tasks_page():
  if request.method == "POST":
    id = int(request.form.get("id"))
    name = request.form.get("name")

    tasks.append(Task(id, name))

  return render_template("tasks.html", tasks=tasks)