import sys
import os
import pytest
from fastapi.testclient import TestClient
sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))


def test_home(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200

def test_login_page(client: TestClient):
    response = client.get("/login")
    assert response.status_code == 200

def test_register_page(client: TestClient):
    response = client.get("/register")
    assert response.status_code == 200


def test_dashboard_authorized(client: TestClient):
    client.post("/register", data={"username": "testuser", "password": "testpassword"})

    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text

    cookies = login_response.cookies

    response = client.get("/dashboard", cookies=cookies)

    assert response.status_code == 200, response.text


def test_deposit_balance(client: TestClient):
    client.post("/register", data={"username": "testuser", "password": "testpassword"})

    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text

    cookies = login_response.cookies

    response = client.post("/balance", data={"amount": 50}, cookies=cookies)
    assert response.status_code in [200, 303]


def test_select_model(client: TestClient):
    client.post("/register", data={"username": "testuser", "password": "testpassword"})

    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text

    cookies = login_response.cookies
    response = client.post("/select_model", data={"data": "resnet50"}, cookies=cookies)
    assert response.status_code in [200, 303]


def test_logout(client: TestClient):
    client.post("/register", data={"username": "testuser", "password": "testpassword"})

    login_response = client.post("/login", data={"username": "testuser", "password": "testpassword"})
    assert login_response.status_code == 200, login_response.text

    cookies = login_response.cookies
    response = client.post("/logout", cookies=cookies)
    assert response.status_code in [200, 303]
