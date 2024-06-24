def test_status_response_existant_project(client, seed_project):
  response = client.get("/projects/1")
  assert response.status_code == 200

def test_status_response_non_existant_project(client, seed_project):
  response = client.get("/projects/2")
  assert response.status_code == 404

def test_title_of_project(client, seed_project):
  response = client.get("/projects/1")
  project_title = "<h1>Project 1</h1>"
  assert project_title in response.text

def test_quantity_of_tasks(client, seed_project):
  response = client.get("/projects/1")
  task_cards = '<section class="task-project">'
  assert response.text.count(task_cards) == 2

def test_title_of_tasks(client, seed_project):
  response = client.get("/projects/1")
  task_1 = "<p>Task 1</p>"
  task_2 = "<p>Task 2</p>"
  assert task_1 in response.text
  assert task_2 in response.text