import streamlit as st
import requests

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

                # Vérifier si l'API renvoie une erreur pour ce client
                if "error" in result:
                    st.error(result["error"])
                else:
                    st.write("Probabilité de défaut :", round(result["proba"], 2))
                    st.write("Prédiction :", "Défaut" if result["prediction"] == 1 else "Pas de défaut")
            else:
                st.error(f"Erreur API : {response.status_code} - {response.text}")

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")
