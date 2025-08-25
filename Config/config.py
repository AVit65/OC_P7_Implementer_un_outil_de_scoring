# config.py
import os
from pathlib import Path

# Répertoire du script
BASE_DIR = Path(__file__).resolve().parent

# Chemins vers les ressources
PIPELINE_PATH = BASE_DIR.parent / "Output" / "Pipelines" / "pipeline_to_deployed.joblib"
CLIENT_PATH = BASE_DIR.parent / "Output" / "Data_clients" / "App_test_final.csv"
VAR_DESC_PATH = BASE_DIR.parent / "Output" / "Variables" / "Variable_description.csv"
SHAP_VALUE_TEST_PATH = BASE_DIR.parent / "Output" / "Shap_value" / "shap_value_test.joblib"
SHAP_VALUE_TRAIN_PATH = BASE_DIR.parent / "Output" / "Shap_value" / "shap_value_train.joblib"
RAW_DATA_TEST_ALIGNED_PATH = BASE_DIR.parent / "Output" / "Shap_value" / "raw_data_test_with_colname_aligned.csv"
VARIABLE_TYPE_PATH = BASE_DIR.parent / "Output" / "Variables" / "Variable_type.csv"
LOGO_PATH = BASE_DIR.parent  / "Images" / "Logo.png"

# Hyperparamètres / seuils
DEFAULT_THRESHOLD = float(os.getenv("THRESHOLD", 0.53))
DEFAULT_PORT = int(os.getenv("PORT", 8001))
