# Import des librairies
#---------------------------------------------------------------------

import sys
import os
from fastapi.testclient import TestClient
from pathlib import Path
import sys


# Import des librairies
#---------------------------------------------------------------------

# Définition du chemin absolu du dossier du script
script_dir = Path(__file__).resolve().parent

# Définition du chemin vers le dossier API 
api_path = script_dir.parent / "API"

# Ajoute le chemin au path Python pour pouvoir importer app.py
sys.path.append(str(api_path))

# Importation de l'application
from api import app

# Préparation
#---------------------------------------------------------------------

# Initialisation du client de test
client = TestClient(app)

# Test de la racine 
#--------------------------------------------------------------------------------------

def test_read_root():

    # Envoie d'une requête get
    response = client.get("/")

    # Verrification que le code HTTP envoyé est 200
    assert response.status_code == 200

    # Verrification que la réponse JSON correspond au message envoyé
    assert response.json() == {"message": "Bienvenue sur mon API ML !"}

# Test de la route predict avec un client existant
#--------------------------------------------------------------------------------------


def test_predict_success():
    
    # Définition d'un client existant dans les données
    clientid = {"client_id": 396899} 

    # Envoie d'une requête post avec le client définit
    response = client.post("/predict", json=clientid)
    
    # Verrification que le code HTTP envoyé est 200
    assert response.status_code == 200

    # Conversion de la réponse en dictionnaire
    data = response.json()

    # Verrification que la réponse contient les clés prédiction et proba
    assert "prediction" in data
    assert "proba" in data

# Test de la route predict avec un client inexistant
#--------------------------------------------------------------------------------------


def test_predict_client_not_found():
    
    # Définition d'un client inexistant dans les données
    clientid = {"client_id": 999999999}

    # Envoie d'une requête post avec le client définit
    response = client.post("/predict", json=clientid)

    # Verrification que le code HTTP envoyé est 422
    assert response.status_code == 200 

    # Conversion de la réponse en dictionnaire 
    data = response.json()

    # Verrification que la réponse contient les clés erreor avec le message non trouvé
    assert "error" in data
    assert "non trouvé" in data["error"]

# Test de la validation des entrée pour la route predict 
#--------------------------------------------------------------------------------------

def test_predict_validation_error():
    
    # Définition d'un id client non valide
    clientid = {}  
    
    # Envoie d'une requete post avec le client non valide
    response = client.post("/predict", json=clientid)

    # Verrification que l'API renvoie bien 422
    assert response.status_code == 422

    # Verrification que le réponse contient detail 
    assert "detail" in response.json()
