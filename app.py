"""
Plateforme Data & IA – Santé au Travail
Auteure : Kenewy Diallo
"""

import streamlit as st

st.set_page_config(
    page_title="Plateforme Data & IA – Santé au Travail",
    page_icon="🏥",
    layout="wide",
)

st.title("🏥 Plateforme Data & IA – Santé au Travail")
st.markdown("*Exploitez vos données, automatisez vos processus, pilotez votre activité.*")
st.divider()

col1, col2, col3 = st.columns(3)
with col1:
    st.info("### 🏠 Accueil\nKPI globaux et alertes en temps réel.")
    st.info("### 🔍 Analyse Adhérents\nScoring et détection des adhérents à risque.")
with col2:
    st.success("### 💬 Chatbot IA\nAssistant conversationnel pour les équipes.")
    st.success("### 📋 Générateur Rapports\nRapports automatiques exportables.")
with col3:
    st.warning("### 📣 Campagne Comm.\nCréateur de contenu IA ciblé.")
    st.warning("### 🛡️ Conformité RGPD\nAnonymisation et vérification des données.")

st.divider()
st.caption("Développé par Kenewy Diallo – Analyste Data & IA | Montpellier")
