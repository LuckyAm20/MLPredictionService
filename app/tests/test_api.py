import os
import sys

from pydantic import BaseModel
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


class UserCreate(BaseModel):
    username: str
    password: str

def test_signup(client: TestClient):
    response = client.post("/user/signup", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "user_id" in response.json()

def test_signup_existing_user(client: TestClient):
    response = client.post("user/signup", json={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 409

def test_get_token(client: TestClient):
    response = client.post("user/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_transaction_history(client: TestClient):
    token_response = client.post("/user/token", data={"username": "testuser", "password": "testpassword"})
    token = token_response.json()["access_token"]
    response = client.get("/transaction/history/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
    assert response.json().get('detail') == "История транзакций пуста"


def test_get_balance(client: TestClient):
    token_response = client.post("user/token", data={"username": "testuser", "password": "testpassword"})
    token = token_response.json()["access_token"]
    response = client.get("user/balance", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "balance" in response.json()

def test_deposit_balance(client: TestClient):
    token_response = client.post("user/token", data={"username": "testuser", "password": "testpassword"})
    token = token_response.json()["access_token"]
    response = client.post("user/balance/deposit/100", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "new_balance" in response.json()

def test_select_model(client: TestClient):
    token_response = client.post("user/token", data={"username": "testuser", "password": "testpassword"})
    token = token_response.json()["access_token"]
    response = client.post("user/select_model", json={"model": "resnet50"}, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Вы выбрали модель resnet50"


def test_prediction_history(client: TestClient):
    token_response = client.post("/user/token", data={"username": "testuser", "password": "testpassword"})
    token = token_response.json()["access_token"]
    response = client.get("/prediction/history/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
    assert response.json().get('detail') == "История предсказаний пуста"


def test_transaction_history_full(client: TestClient):
    token_response = client.post("/user/token", data={"username": "testuser", "password": "testpassword"})
    token = token_response.json()["access_token"]
    client.post("user/balance/deposit/100", headers={"Authorization": f"Bearer {token}"})
    response = client.get("/transaction/history/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in [200, 404]
    transaction = response.json()[-1]
    assert transaction['amount'] == 100
    assert transaction['user_id'] == 1
