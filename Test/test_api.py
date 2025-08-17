import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../API")))


from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Bienvenue sur mon API ML !"}

def test_predict_success():
    # Utiliser un client_id présent la table
    payload = {"client_id": 396899}  
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "prediction" in data
    assert "proba" in data

def test_predict_client_not_found():
    # Utiliser un client_id qui n'existe pas
    payload = {"client_id": 999999999}
    response = client.post("/predict", json=payload)
    assert response.status_code == 200  
    data = response.json()
    assert "error" in data
    assert "non trouvé" in data["error"]

def test_predict_validation_error():
    # Champ obligatoire manquant pour forcer une erreur 422
    payload = {}  # client_id manquant
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    assert "detail" in response.json()
