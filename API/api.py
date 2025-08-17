
"""
API de scoring de clients avec FastAPI.

Ce script expose une API REST permettant de :
- Charger un pipeline de machine learning entraîné (fichier .joblib).
- Charger une base de clients (fichier .csv).
- Fournir une route GET "/" pour tester l'API.
- Fournir une route POST "/predict" permettant de prédire le risque
  pour un client donné, en fonction de son identifiant (SK_ID_CURR).

Fonctionnalités principales :
- Gestion des erreurs génériques (Exception) et des erreurs de validation (RequestValidationError),
  avec retour d'une réponse JSON adaptée.
- Logging des événements pour faciliter le suivi.
- Configuration automatique du port via la variable d'environnement PORT (par défaut : 8001).
- Compatibilité avec deux modes de lancement :
  1. python app.py (utilise le bloc `if __name__ == "__main__"`)
  2. uvicorn app:app --reload --port 8001 (recommandé en production)

Auteur : [Aline Vitrac]
Date : [17/08/2025]
"""


# Import des librairies
#---------------------------------------------------------------------

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel
import joblib
import pandas as pd
import uvicorn
import logging
import os

# Préparation
#--------------------------------------------------------------------------------

# Initialisation de l'application
app = FastAPI()

# Gestion des erreurs génériques
@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur non gérée : {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": str(exc)})

# Gestion des erreurs de validation
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}", exc_info=True)
    return JSONResponse(status_code=422, content={"detail": exc.errors()})

# Définition d'un log d'info s'affichant au démarrage
logger = logging.getLogger("uvicorn.error")
logger.info("Démarrage du serveur")

# Chargement des données 
#----------------------------------------------------------------------------------------------

# BASE_DIR = dossier où se trouve app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ROOT_DIR = racine du projet (un niveau au-dessus de API/)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

# Définition du chemin relatif pour charger la pipeline et les données clients
pipeline_path = os.path.join(ROOT_DIR, "Output/Pipelines", "pipeline_to_deployed.joblib")
client_path = os.path.join(ROOT_DIR, "Output/Data_clients", "App_test_final.csv")

# Chargement de la pipeline et de la table client
pipeline = joblib.load(pipeline_path)
clients_df = pd.read_csv(client_path) 

# Définition du modèle d'entrée
#----------------------------------------------------------------------------------------------

class ClientID(BaseModel):
    client_id: int

# Définition des routes de l'API
#----------------------------------------------------------------------------------------------


# Définition de la rtouge d'acceuil
@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API ML !"}

# Définition de la route de prédiction
@app.post("/predict")
async def predict(data: ClientID):
    client_id = data.client_id
    
    # Chercher le client dans la colonne SK_ID_CURR
    client_data = clients_df[clients_df["SK_ID_CURR"] == client_id]
    
    if client_data.empty:
        return {"error": f"Client {client_id} non trouvé"}
    
    seuil = 0.3

    try:
        # Suppression des variables SK_ID_CURR et TARGET avant de prédire
        X = client_data.drop(columns=["SK_ID_CURR", "TARGET"])

        # Calcule des probabilité prédite par le modèle
        proba = pipeline.predict_proba(X)

        # Extraction de la probabilité associé à la classe 1 (risque élevée de défaut de paiment)
        prob_pos = proba[0][1]

        # Prédiction de la classe 1 en fonction du seuil optimisé
        prediction_seuil = 1 if prob_pos >= seuil else 0

        # Sortie de la fonction
        return {
            "prediction": prediction_seuil,
            "proba": prob_pos
        }
    except Exception as e:
        return {"error": str(e)}


# Lancement du serveur
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False, log_level="debug")
