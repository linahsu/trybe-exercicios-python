from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

def test_hello_world():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
    
# A página da documentação que usaremos de referência é https://fastapi.tiangolo.com/tutorial/testing/

# Também há outros materiais de teste mais avançados na documentação da ferramenta: https://fastapi.tiangolo.com/advanced/async-tests/