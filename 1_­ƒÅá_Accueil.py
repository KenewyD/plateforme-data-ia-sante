"""
Page 1 – Accueil : KPI globaux et alertes
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Accueil", page_icon="🏠", layout="wide")
st.title("🏠 Tableau de Bord Global")
st.markdown("*Vue d'ensemble de l'activité et alertes prioritaires.*")
st.divider()

np.random.seed(1)

# ── KPI ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("🏢 Adhérents actifs",     "450",  delta="+12 ce mois")
k2.metric("✅ Visites réalisées",    "1 247", delta="+8% vs N-1")
k3.metric("📈 Taux de réalisation",  "93%",   delta="+3% vs objectif")
k4.metric("⚠️ Alertes ouvertes",     "7",     delta="-2 cette semaine", delta_color="inverse")
k5.metric("💡 Score engagement moy.","68/100", delta="+5 pts")

st.divider()

# ── Alertes ───────────────────────────────────────────────────────────────────
st.subheader("🚨 Alertes Prioritaires")

alertes = [
    {"niveau": "🔴 Critique", "message": "23 adhérents n'ont pas eu de visite depuis +24 mois", "action": "Planifier des visites de rattrapage"},
    {"niveau": "🟠 Important", "message": "Taux de réalisation en baisse sur le secteur BTP (78%)", "action": "Contacter les employeurs BTP"},
    {"niveau": "🟡 Attention", "message": "12 comptes-rendus en attente de validation", "action": "Relancer les médecins concernés"},
    {"niveau": "🟢 Info", "message": "Nouveau pic d'engagement sur les services (+15%)", "action": "Capitaliser sur cette dynamique"},
]

for alerte in alertes:
    with st.expander(f"{alerte['niveau']} — {alerte['message']}"):
        st.markdown(f"**Action recommandée :** {alerte['action']}")

st.divider()

# ── Activité 12 mois ──────────────────────────────────────────────────────────
st.subheader("📅 Activité des 12 derniers mois")

mois = ["Avr-25","Mai","Jun","Jul","Aoû","Sep","Oct","Nov","Déc","Jan-26","Fév","Mar"]
prog = [102,118,95,80,58,116,122,108,103,98,110,115]
real = [97,112,89,75,53,110,116,101,97,92,104,109]

fig = go.Figure()
fig.add_bar(x=mois, y=prog, name="Programmées", marker_color="#CBD5E1")
fig.add_bar(x=mois, y=real, name="Réalisées", marker_color="#2563EB")
fig.update_layout(barmode="overlay", height=320,
                  legend=dict(orientation="h", y=-0.25),
                  margin=dict(t=10, b=0))
st.plotly_chart(fig, use_container_width=True)

# ── Répartition secteurs ──────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    st.subheader("🏭 Répartition adhérents")
    secteurs = pd.DataFrame({
        "secteur": ["Services","Industrie","BTP","Santé","Commerce"],
        "n": [142, 98, 67, 54, 89],
    })
    fig2 = px.pie(secteurs, values="n", names="secteur",
                  color_discrete_sequence=px.colors.sequential.Blues_r, hole=0.4)
    fig2.update_layout(height=300, margin=dict(t=10,b=0))
    st.plotly_chart(fig2, use_container_width=True)

with col2:
    st.subheader("📊 Taux de réalisation par secteur")
    taux = pd.DataFrame({
        "secteur": ["Services","Industrie","BTP","Santé","Commerce"],
        "taux": [96, 91, 78, 98, 89],
    })
    fig3 = px.bar(taux.sort_values("taux"), x="taux", y="secteur",
                  orientation="h", color="taux",
                  color_continuous_scale="RdYlGn",
                  range_color=[70,100], text="taux")
    fig3.add_vline(x=90, line_dash="dash", line_color="red",
                   annotation_text="Objectif 90%")
    fig3.update_traces(texttemplate="%{text}%", textposition="outside")
    fig3.update_layout(coloraxis_showscale=False,
                       height=300, margin=dict(t=10,b=0))
    st.plotly_chart(fig3, use_container_width=True)
