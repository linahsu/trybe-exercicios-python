from src.models.db import db

def test_status_response_existant_task(client, seed_project):
  task = db.get_collection("projects").find_one({ "idProject": 1 })
  response = client.get(f"/task/{task['_id']}")
  assert response.status_code == 200

def test_status_response_non_existant_task(client, seed_project):
  response = client.get("/task/qualquer_id")
  assert response.status_code == 404

def test_title_of_task(client, seed_project):
    task = db.get_collection("projects").find_one({ "idProject": 1 })
    response = client.get(f"/task/{task['_id']}")
    assert task["task"] in response.text