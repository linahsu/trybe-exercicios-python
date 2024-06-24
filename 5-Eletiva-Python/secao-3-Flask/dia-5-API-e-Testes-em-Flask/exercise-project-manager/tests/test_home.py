def test_status_response(client):
  response = client.get("/")
  assert response.status_code == 200

def test_quantity_of_projects(client, seed_project):
  response = client.get("/")
  project_cards = '<section class="project-home">'
  assert response.text.count(project_cards) == 1

def test_quantity_of_tasks(client, seed_project):
  response = client.get("/")
  task_cards = '<section class="task-home">'
  assert response.text.count(task_cards) == 2

def test_title_of_tasks(client, seed_project):
  response = client.get("/")
  task_1 = "<p>Task 1</p>"
  task_2 = "<p>Task 2</p>"
  assert task_1 in response.text
  assert task_2 in response.text