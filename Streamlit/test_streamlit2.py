import streamlit as st
import requests
import plotly.graph_objects as go

# === Mise en page en colonnes ===
col1, col2 = st.columns([1, 2])  # gauche = image, droite = tout le reste

# Colonne gauche = image
with col1:
    st.image(
    "../Images/Logo.png")


# Colonne droite = tout ton app actuelle
with col2:
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
                url = "http://localhost:8001/predict"  
                payload = {"client_id": int(client_id)}
                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    result = response.json()

                    if "error" in result:
                        st.error(result["error"])
                    else:
                        proba = result["proba"]

                        st.write("### Résultats du modèle")
                        st.write("Probabilité de défaut :", round(proba, 2))
                        st.write("Prédiction :", "⚠️ Défaut" if result["prediction"] == 1 else "✅ Pas de défaut")

                        # Jauge
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=proba * 100,
                            title={'text': "Risque (%)"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkred" if proba > 0.5 else "black"},
                                'steps': [
                                    {'range': [0, 50], 'color': "gold"},
                                    {'range': [50, 100], 'color': "DarkSlateBlue"}
                                ],
                                'threshold': {
                                    'line': {'color': "black", 'width': 4},
                                    'thickness': 0.8,
                                    'value': 50
                                }
                            }
                        ))

                        fig.update_layout(width=350, height=250, margin=dict(l=20, r=20, t=40, b=20))
                        st.plotly_chart(fig, use_container_width=False)

                else:
                    st.error(f"Erreur API : {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'API : {e}")
