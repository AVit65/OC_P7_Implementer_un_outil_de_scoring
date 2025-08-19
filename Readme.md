**CreditRiskScore**

La société Prêt à Dépenser est une société financière  qui propose des crédits à la consommation. 
Dans une logique de gestion du risque, l’entreprise souhaite mettre en place un outil de scoring de crédits capable d’estimer 
la probabilité qu’un client rembourse son emprunt. Cet outil permettra de classer automatiquement les demandes en deux catégories : 
les demandes de prêts peu risquées qui seront acceptées ou les demandes de prêts risquées qui seront refusées. Pour déveloper ce modèle 
de classification, la société fournit un large pannel de données provenant de différentes sources et inclus des informations comportementales 
et des données issues d'autres institutions financières.

**Architecture du repository**

```
OC_projet_7/
│
├── README.md                                   # Documentation générale du projet
├── requirements.txt                            # Liste des dépendances Python nécessaires
├── .gitignore                                  # Liste des fichiers et dossiers à ignorer par Git
├── Procfile                                    # Fichier de configuration pour le déploiement 
├── .python-version                             # Version de Python utilisée 
│
├── .github/workflows/                          # Dossier contenant les workflows GitHub Actions 
│   ├── deployed.yml                            # Workflow de déploiement automatique de l’API
│   └── test.yml                                # Workflow de tests automatisés 
│
├── Data/
      
├── Output/                                     # Données et modèles sauvegardés
│   ├── Data/clients/App_test_final.csv         # Jeu de données client test pour l'API
│   └── Pipelines/pipeline_to_deployed.joblib   # Pipeline de machine learning pré entraîné
│
├── notebooks/                                  # Notebooks d’exploration, d’analyse et de modélisation
│
├── API/                                        # Code source de l’API
│   ├── __init__.py                             # Fichier d’initialisation 
│   └── api.py                                  # Script principal de l’API
│
└── Test/                                       # Scripts de test
    ├── __init__.py                             # Fichier d’initialisation 
    └── test_api.py                             # Tests unitaires de l’API

```
**Données**

Les tables de données brutes listées ci-dessous et utilisées dans les notebook d'exploration, de modélisation et d'analyse de dérive peuvent être téléchargées sur [Kaggle]( https://www.kaggle.com/c/home-credit-default-risk/data)  

- application_{train|test}.csv
- bureau.csv
- bureau_balance.csv
- POS_CASH_balance.csv
- credit_card_balance.csv
- previous_application.csv
- installments_payments.csv
- HomeCredit_columns_description.csv

**Lien vers le dashboard et vers l'API** 

- API: https://api-oc-p7.onrender.com/docs#/  
- Dashboard : https://oc-p7-cu77.onrender.com/

