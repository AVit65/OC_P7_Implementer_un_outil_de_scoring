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


# chemin absolu basé sur le script b
script_dir = Path(__file__).resolve().parent
logo_path = script_dir.parent / "Images" / "Logo.png"

#----------------------------------------------------------------------------------------------------------------------
# Menu
#----------------------------------------------------------------------------------------------------------------------

# Sidebar pour la navigation
st.sidebar.title("Menu")
section = st.sidebar.radio("Choisir une section :", ["Présentation du Dashboard", "Présentation de l'outil", 
                                                     "Outil d'aide à la décision", "Description des variables"])

#----------------------------------------------------------------------------------------------------------------------
# Section Présentation
#----------------------------------------------------------------------------------------------------------------------


if section == "Présentation du Dashboard":

    # Ajout d'un logo
    st.image(str(logo_path), use_column_width=True)

    st.header("Présentation du Dashboard")
    st.markdown("""
    Ce dashboard permet de visualiser les résultats de prédictions de la proabilité de défaut de paiment d'un client demandant un crédit. 
    Le modèle a été entrainé pour classer les demandes de crédits en deux catégories :
                
    - les demandes jugées peu risquées, qui pourront être acceptées,
    - les demandes jugées risquées, qui seront refusées.
    
    Une présentation de l'outil est disponible dans la section <u><i> Presentation de l'outil </i></u>
                
    Pour obtenir la classe prédite par le modèle, seul l'identitiant de la demande est nécessaire. Les résultats peuvent être
    visualisés sous la forme d'une jauge qui indique le niveau de risque de la demande dans la section 
    <u><i>Outil d'aide à la décesion</i></u>.
    A noter que le seuil utilisé pour décider si une demande est risquée ou non a été ajusté en fonction de critères définis par 
    les équipes métier afin de mieux refléter la réalité du risque. Ici le seuil utilisé est de . 
    
    Ainsi les demandes dont la probabilité est inférieure à
    seront jugées comment peu risquées et les demandes supérieur à ce seuil seront jugée comme risquées.
                
            
    Le modèle a été construit à partir de différentes sources de données. Une description des variables utilisée par le 
    modèle est fournie dans la section <u><i>Description des variables</i></u>. 
  
    
    """, unsafe_allow_html=True)                                            



#----------------------------------------------------------------------------------------------------------------------
# Section Outil d'aide à la décision
#----------------------------------------------------------------------------------------------------------------------

elif section == "Outil d'aide à la décision":

    # Ajout d'un logo
    st.image(str(logo_path), use_column_width=True)

    # Ajout d'un titre
    st.header("Prédiction du risque de défaut de paiment d'un client")

    # Saisie manuelle de l'ID client
    client_id = st.number_input("Entrez l'ID de la demande", min_value=0, step=1)
    st.caption("Exemple : 216970")

    # Prédiction
    # --------------------------------------------------------------------------------
    if st.button("Prédire"):
        if client_id < 0:
            st.error("Veuillez entrer un ID de demande valide.")
        else:
            try:
                # Appel API pour prédiction
                url = os.getenv("API_URL", "http://localhost:8001/predict")
                payload = {"client_id": int(client_id)}
                response = requests.post(url, json=payload)

                if response.status_code == 200:
                    result = response.json()

                    # Gestion du cas où l'API renverrait une erreur
                    if "error" in result:
                        st.error(result["error"])
                    else:
                        # Stockage des résultats dans session_state
                        st.session_state.proba = result["proba"]
                        st.session_state.prediction = result["prediction"]

                else:
                    st.error(f"Erreur API : {response.status_code} - {response.text}")

            except Exception as e:
                st.error(f"Erreur lors de l'appel à l'API : {e}")

    # Affichage d'une jauge 
    # --------------------------------------------------------------------------------
    if "proba" in st.session_state:
        proba = st.session_state.proba
        st.write("Probabilité de défaut :", round(proba, 2))
        st.write("La demande a été classée comme risquée"
                 if st.session_state.prediction == 1 else "La demande a été classée comme peu risquée")

        # Ajout de la jauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=proba * 100,
            number={'suffix': "%"},
            title={'text': "Risque (%)"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "black"},
                'steps': [
                    {'range': [0, 53], 'color': "Gold"},
                    {'range': [53, 100], 'color': "DarkSlateBlue"}
                ],
                'threshold': {'line': {'color': "black", 'width': 4}, 'thickness': 0.8, 'value': 53}
            }
        ))
        fig.update_layout(width=350, height=250, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    # Séparateur après la jauge
    st.markdown("---")