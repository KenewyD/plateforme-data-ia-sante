"""
Page 2 – Analyse Adhérents : Scoring & Détection du risque de départ
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Analyse Adhérents", page_icon="🔍", layout="wide")
st.title("🔍 Analyse Adhérents – Scoring & Risque de Départ")
st.markdown("*Identifiez les adhérents à risque et priorisez vos actions de fidélisation.*")
st.divider()

@st.cache_data
def generate_adherents(n=300):
    np.random.seed(42)
    df = pd.DataFrame({
        "id": range(1, n+1),
        "secteur": np.random.choice(["Services","Industrie","BTP","Santé","Commerce"], n),
        "effectif": np.random.randint(5, 500, n),
        "anciennete_mois": np.random.randint(1, 72, n),
        "nb_visites_annee": np.random.randint(0, 15, n),
        "nb_reclamations": np.random.randint(0, 5, n),
        "taux_reponse_enquete": np.random.uniform(0, 1, n).round(2),
        "retard_paiement_jours": np.random.randint(0, 90, n),
        "nb_contacts_support": np.random.randint(0, 10, n),
    })

    # Score de risque (0 = stable, 100 = très à risque)
    df["score_risque"] = (
        (1 - df["nb_visites_annee"] / 15) * 30
        + (df["nb_reclamations"] / 5) * 25
        + (1 - df["taux_reponse_enquete"]) * 20
        + (df["retard_paiement_jours"] / 90) * 15
        + (df["nb_contacts_support"] / 10) * 10
    ).round(1)

    df["risque"] = pd.cut(df["score_risque"],
        bins=[0, 25, 50, 75, 100],
        labels=["🟢 Stable", "🟡 Surveillance", "🟠 À risque", "🔴 Critique"])

    df["segment_taille"] = pd.cut(df["effectif"],
        bins=[0,9,49,249,float("inf")],
        labels=["TPE","PME","ETI","Grande"])

    return df

df = generate_adherents()

# ── Filtres ───────────────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    secteur_f = st.multiselect("🏭 Secteur", df["secteur"].unique(), default=df["secteur"].unique())
with col_f2:
    risque_f = st.multiselect("⚠️ Niveau de risque", df["risque"].dropna().unique(), default=df["risque"].dropna().unique())
with col_f3:
    taille_f = st.multiselect("🏢 Taille", df["segment_taille"].dropna().unique(), default=df["segment_taille"].dropna().unique())

dff = df[df["secteur"].isin(secteur_f) & df["risque"].isin(risque_f) & df["segment_taille"].isin(taille_f)]

st.divider()

# ── KPI ───────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)
k1.metric("📋 Adhérents analysés", len(dff))
k2.metric("🔴 Critiques", len(dff[dff["risque"] == "🔴 Critique"]))
k3.metric("🟠 À risque", len(dff[dff["risque"] == "🟠 À risque"]))
k4.metric("📊 Score risque moyen", f"{dff['score_risque'].mean():.1f}/100")

st.divider()

# ── Graphiques ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Distribution des scores de risque")
    fig1 = px.histogram(dff, x="score_risque", nbins=20,
                        color_discrete_sequence=["#2563EB"])
    fig1.add_vline(x=75, line_dash="dash", line_color="red",
                   annotation_text="Seuil critique")
    fig1.add_vline(x=50, line_dash="dash", line_color="orange",
                   annotation_text="Seuil à risque")
    fig1.update_layout(height=320, margin=dict(t=10,b=0))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("🏭 Risque par secteur")
    cross = dff.groupby(["secteur","risque"], observed=True).size().reset_index(name="n")
    colors = {"🟢 Stable":"#22C55E","🟡 Surveillance":"#F59E0B",
              "🟠 À risque":"#F97316","🔴 Critique":"#EF4444"}
    fig2 = px.bar(cross, x="secteur", y="n", color="risque",
                  color_discrete_map=colors, barmode="stack")
    fig2.update_layout(height=320, margin=dict(t=10,b=0),
                       legend=dict(orientation="h", y=-0.3))
    st.plotly_chart(fig2, use_container_width=True)

# ── Scatter ───────────────────────────────────────────────────────────────────
st.subheader("🎯 Score de risque vs Ancienneté")
fig3 = px.scatter(dff, x="anciennete_mois", y="score_risque",
                  color="risque", color_discrete_map=colors,
                  size="effectif", hover_data=["secteur","segment_taille"],
                  opacity=0.7)
fig3.add_hline(y=75, line_dash="dash", line_color="red")
fig3.update_layout(height=380, margin=dict(t=10,b=0))
st.plotly_chart(fig3, use_container_width=True)

# ── Liste critiques ───────────────────────────────────────────────────────────
st.subheader("🔴 Adhérents Critiques – Actions prioritaires")
critiques = dff[dff["risque"] == "🔴 Critique"].sort_values("score_risque", ascending=False).head(10)
critiques_display = critiques[["id","secteur","segment_taille","anciennete_mois",
                                "nb_reclamations","retard_paiement_jours","score_risque","risque"]].copy()
critiques_display.columns = ["ID","Secteur","Taille","Ancienneté (mois)",
                              "Réclamations","Retard paiement (j)","Score risque","Niveau"]
st.dataframe(critiques_display, use_container_width=True, hide_index=True)

csv = dff[dff["risque"].isin(["🔴 Critique","🟠 À risque"])].to_csv(index=False).encode("utf-8")
st.download_button("📥 Exporter les adhérents à risque (.csv)", data=csv,
                   file_name="adherents_a_risque.csv", mime="text/csv")
