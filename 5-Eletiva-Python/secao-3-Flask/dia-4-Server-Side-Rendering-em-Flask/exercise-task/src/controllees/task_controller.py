from flask import Blueprint, render_template
from models.task_model import Task

tasks = [
  Task(1, "lavar roupas"),
  Task(2, "beber água"),
  Task(3, "fazer almoço"),
]