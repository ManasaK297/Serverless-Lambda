import sys
print(sys.path)
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.main import app
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_deploy_and_execute():
    response = client.post("/deploy/", json={"name": "hello", "code": "print('Hello World')"})
    assert response.status_code == 200
    function_id = response.json()["function_id"]

    exec_response = client.post(f"/execute/{function_id}")
    assert "Hello World" in exec_response.json()["output"]
