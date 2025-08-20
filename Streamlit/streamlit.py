# Import des librairies
#---------------------------------------------------------------------

import streamlit as st
import requests
import plotly.graph_objects as go
import os
from pathlib import Path


# chemin absolu basé sur le script b
script_dir = Path(__file__).resolve().parent
logo_path = script_dir.parent / "Images" / "Logo.png"

# Ajout d'un logo
st.image(str(logo_path))

# Ajout d'un titre
st.title("Prédiction du risque de défaut de paiment d'un client")

# Saisie manuelle de l'ID client
client_id = st.number_input("Entrez l'ID du client", min_value=0, step=1)

# Bouton pour prédire
if st.button("Prédire"):
    if client_id < 0:
        st.error("Veuillez entrer un ID client valide.")
    else:
        try:
            # Appel API
            url = os.getenv("API_URL", "http://localhost:8001/predict")
            payload = {"client_id": int(client_id)}
            response = requests.post(url, json=payload)
            
            if response.status_code == 200:
                result = response.json()

                # Gestion du cas où l'API renverrait une erreur
                if "error" in result:
                    st.error(result["error"])
                else:
                    proba = result["proba"]
                    st.write("Probabilité de défaut :", round(proba, 2))
                    st.write("Le client a été classé comme mauvais payeur" if result["prediction"] == 1 else "Le client a été classé comme bon payeur")

                    # Ajout de la jauge
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = proba * 100,  
                        number = {'suffix': "%"},
                        title = {'text': "Risque (%)"},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkred" if proba > 0.5 else "black"},
                            'steps': [
                                {'range': [0, 53], 'color': "Gold"},
                                {'range': [53, 100], 'color': "DarkSlateBlue"}
                            ],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.8,
                                'value': 53 
                            }
                        }
                    ))

                    fig.update_layout(width=350, height=250, margin=dict(l=20, r=20, t=40, b=20))

                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Erreur API : {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")
