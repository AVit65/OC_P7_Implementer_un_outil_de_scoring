import streamlit as st
import requests
import plotly.graph_objects as go
import os
from pathlib import Path


# chemin absolu basé sur le script b
script_dir = Path(__file__).resolve().parent
logo_path = script_dir.parent / "Images" / "Logo.png"

st.image(str(logo_path))

st.title("Prédiction de risque client")

# Saisie manuelle de l'ID client
client_id = st.number_input("Entrez l'ID du client", min_value=0, step=1)

# Bouton pour prédire
if st.button("Prédire"):
    if client_id == 0:
        st.error("Veuillez entrer un ID client valide.")
    else:
        try:
            # Appel API
            url = os.getenv("API_URL", "http://localhost:8001/predict")
            payload = {"client_id": int(client_id)}
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                result = response.json()

                # Vérifier si l'API renvoie une erreur pour ce client
                if "error" in result:
                    st.error(result["error"])
                else:
                    proba = result["proba"]
                    st.write("Probabilité de défaut :", round(proba, 2))
                    st.write("Le risque de défaut de paiment est élevée" if result["prediction"] == 1 else "Le risque de défaut de paiment est faible")

                    # === Ajout de la jauge ===
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = proba * 100,  # pourcentage
                        title = {'text': "Risque (%)"},
                        gauge = {
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "darkred" if proba > 0.5 else "black"},
                            'steps': [
                                {'range': [0, 45], 'color': "Gold"},
                                {'range': [45, 100], 'color': "DarkSlateBlue"}
                            ],
                            'threshold': {
                                'line': {'color': "black", 'width': 4},
                                'thickness': 0.8,
                                'value': 45 # seuil par défaut
                            }
                        }
                    ))

                    fig.update_layout(width=350, height=250, margin=dict(l=20, r=20, t=40, b=20))

                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.error(f"Erreur API : {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")