import pytest
from src.app import app
from src.models.db import db
from src.models.projectModel import ProjectModel


@pytest.fixture
def client():
  app.testing = True
  return app.test_client()

@pytest.fixture
def seed_project():
  db.get_collection("projects").drop()

  ProjectModel(
      {
          "idProject": 1,
          "name": "Project 1",
          "task": "Task 1",
          "status": "To Do",
          "completionPercentage": 0,
          "descriptionTask": "Description Task 1",
          "deadline": "2024-08-01",
          "responsible": "Responsible 1",
      }
  ).save()

  ProjectModel(
      {
          "idProject": 1,
          "name": "Project 1",
          "task": "Task 2",
          "status": "Doing",
          "completionPercentage": 50,
          "descriptionTask": "Description Task 2",
          "deadline": "2024-08-02",
          "responsible": "Responsible 2",
      }
  ).save()