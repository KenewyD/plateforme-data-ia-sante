"""
Page 4 – Générateur de Rapports : export Word/PDF
"""
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Générateur Rapports", page_icon="📋", layout="centered")
st.title("📋 Générateur de Rapports Automatiques")
st.markdown("*Créez des rapports professionnels en quelques secondes, exportables en .txt ou .md.*")
st.divider()

mode = st.radio("Mode", ["🎯 Démo", "🔑 Réel (OpenAI)"], horizontal=True)
api_key = None
if mode == "🔑 Réel (OpenAI)":
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input("Clé API", type="password", placeholder="sk-...")
    if not api_key:
        st.warning("Entrez votre clé API.")
        st.stop()

st.divider()

# ── Type de rapport ───────────────────────────────────────────────────────────
type_rapport = st.selectbox("📄 Type de rapport", [
    "Bilan mensuel d'activité",
    "Rapport de visite médicale",
    "Compte-rendu de réunion",
    "Rapport de prévention des risques",
    "Bilan annuel de santé au travail",
])

st.subheader("📝 Données à inclure")

donnees_rapport = {}

if type_rapport == "Bilan mensuel d'activité":
    col1, col2 = st.columns(2)
    with col1:
        donnees_rapport["mois"] = st.text_input("Mois", "Avril 2026")
        donnees_rapport["visites_programmees"] = st.number_input("Visites programmées", value=115)
        donnees_rapport["visites_realisees"] = st.number_input("Visites réalisées", value=108)
    with col2:
        donnees_rapport["nb_adherents"] = st.number_input("Nb adhérents actifs", value=450)
        donnees_rapport["nb_actions_prevention"] = st.number_input("Actions de prévention", value=3)
        donnees_rapport["incidents"] = st.number_input("Incidents signalés", value=2)
    donnees_rapport["points_saillants"] = st.text_area("Points saillants (un par ligne)",
        "Pic d'activité sur le secteur industrie\nNouveau protocole de suivi TMS mis en place")
    donnees_rapport["actions_mois_suivant"] = st.text_area("Actions mois suivant (un par ligne)",
        "Former 2 médecins au nouveau logiciel\nLancer enquête satisfaction adhérents")

elif type_rapport == "Rapport de prévention des risques":
    donnees_rapport["service"] = st.text_input("Service / Entreprise", "Entreprise XYZ")
    donnees_rapport["date"] = st.date_input("Date").strftime("%d/%m/%Y")
    donnees_rapport["risques"] = st.text_area("Risques identifiés (un par ligne)",
        "TMS – postes administratifs\nRisques psychosociaux – service client\nChutes – entrepôt")
    donnees_rapport["mesures_existantes"] = st.text_area("Mesures déjà en place",
        "Ergonomie des postes révisée en 2024\nFormation gestes & postures annuelle")
    donnees_rapport["recommandations"] = st.text_area("Nouvelles recommandations",
        "Audit psychosocial à planifier\nInstaller des sols anti-dérapants entrepôt")

else:
    donnees_rapport["titre"] = st.text_input("Titre", f"{type_rapport} – {datetime.now().strftime('%B %Y')}")
    donnees_rapport["contexte"] = st.text_area("Contexte / Informations générales",
        "Réunion mensuelle de suivi d'activité\nParticipants : Direction, RH, Médecins")
    donnees_rapport["points_cles"] = st.text_area("Points clés à inclure (un par ligne)",
        "Point sur les visites médicales\nBilan des actions de prévention\nPerspectives du mois suivant")
    donnees_rapport["conclusions"] = st.text_area("Conclusions et décisions",
        "Maintien des objectifs\nNouveau planning de visites validé")

ton = st.selectbox("🎨 Ton", ["Professionnel", "Synthétique", "Détaillé"])
st.divider()

# ── Démo ──────────────────────────────────────────────────────────────────────
DEMO_RAPPORT = """# BILAN MENSUEL D'ACTIVITÉ – Avril 2026

**Service de Santé au Travail**
📅 Période : Avril 2026 | 📋 Rapport généré automatiquement

---

## 1. Synthèse Exécutive

Le mois d'avril 2026 affiche des résultats **satisfaisants** avec un taux de réalisation des visites de **93,9%**, au-dessus de l'objectif fixé à 90%.

---

## 2. Activité Médicale

| Indicateur | Valeur | Vs objectif |
|---|---|---|
| Visites programmées | 115 | — |
| Visites réalisées | 108 | ✅ 93,9% |
| Adhérents actifs | 450 | ✅ +12 vs mars |
| Actions de prévention | 3 | ✅ Objectif atteint |
| Incidents signalés | 2 | ⚠️ À surveiller |

---

## 3. Points Saillants

- 📈 **Pic d'activité** observé sur le secteur industrie (+18% vs mars)
- 🛡️ **Nouveau protocole TMS** déployé avec succès sur 3 entreprises adhérentes
- ⚠️ 2 incidents signalés en cours d'investigation

---

## 4. Actions du Mois Suivant

| Action | Responsable | Délai |
|---|---|---|
| Formation logiciel (2 médecins) | Direction médicale | 15/05/2026 |
| Lancement enquête satisfaction | Équipe communication | 20/05/2026 |

---

## 5. Conclusion

Mois positif. La dynamique de réalisation est maintenue. Les 2 incidents feront l'objet d'un suivi spécifique en mai.

---
*Rapport généré automatiquement par la Plateforme Data & IA | Kenewy Diallo*
"""

def build_prompt(type_rapport, ton, donnees):
    instr = {"Professionnel": "Style formel, vocabulaire précis.",
             "Synthétique": "Concis, bullet points, max 300 mots.",
             "Détaillé": "Développé, exhaustif avec tableaux."}[ton]
    return f"""{instr}
Génère un rapport de type "{type_rapport}" professionnel en Markdown.
NE MENTIONNE AUCUNE DONNÉE NOMINATIVE. RGPD.
Données : {donnees}
Structure : Titre > Synthèse > Corps > Tableau récap > Conclusion
"""

if st.button("✨ Générer le rapport", type="primary", use_container_width=True):
    with st.spinner("Génération en cours..."):
        if mode == "🎯 Démo":
            resultat = DEMO_RAPPORT
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Tu es expert en rédaction de rapports pour un service de santé au travail. RGPD strict."},
                        {"role": "user", "content": build_prompt(type_rapport, ton, donnees_rapport)},
                    ],
                    temperature=0.3, max_tokens=2000,
                )
                resultat = response.choices[0].message.content
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.stop()

    st.success("✅ Rapport généré !")
    st.divider()
    st.markdown(resultat)
    st.divider()

    col1, col2 = st.columns(2)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    with col1:
        st.download_button("📄 Télécharger (.md)", data=resultat,
            file_name=f"rapport_{ts}.md", mime="text/markdown", use_container_width=True)
    with col2:
        st.download_button("📝 Télécharger (.txt)", data=resultat,
            file_name=f"rapport_{ts}.txt", mime="text/plain", use_container_width=True)

st.divider()
st.caption("🔒 Aucune donnée nominative transmise. Conforme RGPD.")
