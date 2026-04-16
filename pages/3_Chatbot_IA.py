"""
Page 3 – Chatbot IA : Assistant conversationnel métier
"""
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Chatbot IA", page_icon="💬", layout="centered")
st.title("💬 Assistant IA – Chatbot Métier")
st.markdown("*Posez vos questions métier, obtenez des réponses expertes instantanément.*")
st.divider()

# ── Mode ──────────────────────────────────────────────────────────────────────
mode = st.radio("Mode", ["🎯 Démo", "🔑 Réel (OpenAI)"], horizontal=True)

api_key = None
if mode == "🔑 Réel (OpenAI)":
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input(
        "Clé API OpenAI", type="password", placeholder="sk-...")
    if not api_key:
        st.warning("Entrez votre clé API.")
        st.stop()

# ── Contexte métier ───────────────────────────────────────────────────────────
contexte = st.selectbox("🏥 Contexte", [
    "Médecin du travail",
    "Équipe administrative",
    "Équipe communication / marketing",
    "Direction générale",
])

SYSTEM_PROMPT = f"""Tu es un assistant IA expert pour un service de santé au travail.
Tu réponds aux questions de l'utilisateur qui est dans l'équipe : {contexte}.
Tu es précis, professionnel et tu respectes strictement la confidentialité des données (RGPD).
Tu ne fournis jamais d'informations nominatives sur des salariés ou adhérents.
Réponds en français, de manière concise et utile."""

# ── Réponses démo ─────────────────────────────────────────────────────────────
DEMO_RESPONSES = {
    "visite": "La visite médicale périodique doit être réalisée selon la périodicité définie par le médecin du travail, en fonction des risques du poste. Pour les postes à risques particuliers, la périodicité maximale est de 2 ans.",
    "rgpd": "Dans le cadre du RGPD, les données de santé des salariés sont des données sensibles. Leur traitement nécessite une base légale spécifique, une durée de conservation définie et des mesures de sécurité renforcées. Le DPO doit être consulté.",
    "tms": "Les TMS (Troubles Musculo-Squelettiques) sont la première cause de maladie professionnelle. Les actions préventives incluent : l'analyse ergonomique des postes, la formation aux gestes et postures, et des pauses régulières.",
    "kpi": "Les KPI clés pour un service de santé au travail sont : taux de réalisation des visites, délai de prise en charge, taux d'inaptitude, nombre d'actions de prévention collective, et satisfaction des adhérents.",
    "default": "Je suis votre assistant IA spécialisé en santé au travail. Je peux vous aider sur la réglementation, les procédures médicales, la gestion des données adhérents, ou les actions de prévention. Quelle est votre question ?",
}

def get_demo_response(question):
    q = question.lower()
    if any(w in q for w in ["visite","médical","périodique"]): return DEMO_RESPONSES["visite"]
    if any(w in q for w in ["rgpd","données","confidential"]): return DEMO_RESPONSES["rgpd"]
    if any(w in q for w in ["tms","trouble","musculo"]): return DEMO_RESPONSES["tms"]
    if any(w in q for w in ["kpi","indicateur","performance"]): return DEMO_RESPONSES["kpi"]
    return DEMO_RESPONSES["default"]

# ── Chat ──────────────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# Affichage historique
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Suggestions rapides
if not st.session_state.messages:
    st.markdown("**💡 Questions suggérées :**")
    cols = st.columns(2)
    suggestions = [
        "Quels sont les KPI clés à suivre ?",
        "Comment gérer les données RGPD ?",
        "Quelle est la fréquence des visites médicales ?",
        "Comment prévenir les TMS ?",
    ]
    for i, suggestion in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state.messages.append({"role": "user", "content": suggestion})
                if mode == "🎯 Démo":
                    response = get_demo_response(suggestion)
                else:
                    import openai
                    client = openai.OpenAI(api_key=api_key)
                    res = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role":"system","content":SYSTEM_PROMPT}] + st.session_state.messages,
                        temperature=0.4, max_tokens=600,
                    )
                    response = res.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# Saisie libre
if prompt := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Réflexion..."):
            if mode == "🎯 Démo":
                response = get_demo_response(prompt)
            else:
                import openai
                client = openai.OpenAI(api_key=api_key)
                res = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role":"system","content":SYSTEM_PROMPT}] + st.session_state.messages,
                    temperature=0.4, max_tokens=600,
                )
                response = res.choices[0].message.content
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})

# Reset
if st.session_state.messages:
    if st.button("🗑️ Effacer la conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.divider()
st.caption("🔒 Aucune donnée nominative ne doit être partagée dans ce chat. Conforme RGPD.")
