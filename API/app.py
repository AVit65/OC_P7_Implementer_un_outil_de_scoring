
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import uvicorn
import logging
import os
import joblib

from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(Exception)
async def all_exception_handler(request: Request, exc: Exception):
    logger.error(f"Erreur non gérée : {exc}", exc_info=True)
    return JSONResponse(status_code=500, content={"detail": str(exc)})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(f"Validation error: {exc}", exc_info=True)
    return JSONResponse(status_code=422, content={"detail": exc.errors()})


logger = logging.getLogger("uvicorn.error")
logger.error("Démarrage du serveur avec log_level DEBUG")








# Chargement du pipeline ML 




# BASE_DIR = dossier où se trouve app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ROOT_DIR = racine du projet (un niveau au-dessus de API/)
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))

pipeline_path = os.path.join(ROOT_DIR, "Output/Pipelines", "pipeline_to_deployed.joblib")
client_path = os.path.join(ROOT_DIR, "Output/Data_clients", "App_test_final.csv")

pipeline = joblib.load(pipeline_path)
clients_df = pd.read_csv(client_path) 


class ClientID(BaseModel):
    client_id: int


@app.get("/")
def read_root():
    return {"message": "Bienvenue sur mon API ML !"}

@app.post("/predict")
async def predict(data: ClientID):
    client_id = data.client_id
    
    # Chercher le client dans la colonne SK_ID_CURR
    client_data = clients_df[clients_df["SK_ID_CURR"] == client_id]
    
    if client_data.empty:
        return {"error": f"Client {client_id} non trouvé"}
    
    seuil = 0.3

    try:
        # Retirer SK_ID_CURR avant de prédire
        X = client_data.drop(columns=["SK_ID_CURR"])
        X = client_data.drop(columns=["TARGET"])

        proba = pipeline.predict_proba(X)
        prob_pos = proba[0][1]
        prediction_seuil = 1 if prob_pos >= seuil else 0

        return {
            "prediction": prediction_seuil,
            "proba": prob_pos
        }
    except Exception as e:
        return {"error": str(e)}




if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8001))
    uvicorn.run("app:app", host="0.0.0.0", port=port, reload=False, log_level="debug")
