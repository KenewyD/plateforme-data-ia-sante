"""
Page 5 – Campagne Communication : Créateur de contenu IA
"""
import streamlit as st
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Campagne Communication", page_icon="📣", layout="centered")
st.title("📣 Campagne Communication – Créateur de Contenu IA")
st.markdown("*Générez en quelques secondes des emails, posts et newsletters adaptés à votre audience.*")
st.divider()

mode = st.radio("Mode", ["🎯 Démo", "🔑 Réel (OpenAI)"], horizontal=True)
api_key = None
if mode == "🔑 Réel (OpenAI)":
    api_key = os.getenv("OPENAI_API_KEY") or st.text_input("Clé API", type="password", placeholder="sk-...")
    if not api_key:
        st.warning("Entrez votre clé API.")
        st.stop()

st.divider()

# ── Paramètres ────────────────────────────────────────────────────────────────
col1, col2 = st.columns(2)
with col1:
    type_contenu = st.selectbox("📝 Type de contenu", [
        "📧 Email de newsletter",
        "📱 Post LinkedIn",
        "📢 Annonce interne",
        "📬 Email de relance adhérent",
        "🎯 Email de réactivation",
    ])
with col2:
    cible = st.selectbox("👥 Audience cible", [
        "Employeurs adhérents",
        "Salariés",
        "Équipes internes",
        "Nouveaux adhérents potentiels",
    ])

col3, col4 = st.columns(2)
with col3:
    ton = st.selectbox("🎨 Ton", ["Professionnel", "Bienveillant", "Dynamique", "Informatif"])
with col4:
    longueur = st.selectbox("📏 Longueur", ["Court (< 100 mots)", "Moyen (100-200 mots)", "Long (200+ mots)"])

sujet = st.text_input("💡 Sujet principal", placeholder="Ex : Rappel visite médicale annuelle, Nouveau service de prévention...")
infos_complementaires = st.text_area("📎 Informations complémentaires (optionnel)",
    placeholder="Ex : Date limite, offre spéciale, contact...", height=80)

st.divider()

# ── Contenus démo ─────────────────────────────────────────────────────────────
DEMO_CONTENUS = {
    "📧 Email de newsletter": """**Objet : Votre santé au travail – Actualités d'avril 2026**

Bonjour,

Ce mois-ci, votre service de santé au travail vous propose :

🔹 **Rappel important** : Les visites médicales périodiques doivent être planifiées avant le 30 juin. Contactez-nous pour organiser les créneaux.

🔹 **Nouveau service** : Nous lançons un atelier de prévention des risques psychosociaux — inscriptions ouvertes.

🔹 **Chiffre du mois** : 94% de taux de réalisation des visites en mars 2026. Merci pour votre confiance !

Pour toute question, notre équipe est disponible au [numéro] ou par email.

Cordialement,
L'équipe Santé au Travail""",

    "📱 Post LinkedIn": """🏥 **La prévention, ça commence avant le problème.**

En tant que service de santé au travail, notre mission va bien au-delà de la visite médicale annuelle.

Nous accompagnons les entreprises sur :
✅ L'analyse des risques professionnels
✅ La prévention des TMS et risques psychosociaux
✅ La formation et sensibilisation des équipes
✅ L'intégration de l'IA dans nos processus métier

La santé au travail de demain se construit aujourd'hui. 💪

#SantéAuTravail #Prévention #RH #BienêtreAuTravail""",

    "📬 Email de relance adhérent": """**Objet : Votre visite médicale – À planifier avant le 30/06**

Bonjour,

Nous n'avons pas encore pu planifier votre visite médicale périodique pour cette année.

Pour rappel, cette visite est **obligatoire** et permet de :
- Vérifier l'aptitude au poste
- Identifier les risques professionnels
- Mettre en place des actions préventives adaptées

📅 **Prenez rendez-vous facilement** en répondant à cet email ou en nous appelant.

Nous restons à votre disposition.

L'équipe médicale""",
}

def build_prompt_comm(type_contenu, cible, ton, longueur, sujet, infos):
    ton_map = {"Professionnel": "formel et professionnel",
               "Bienveillant": "chaleureux et bienveillant",
               "Dynamique": "dynamique et engageant",
               "Informatif": "clair et informatif"}
    long_map = {"Court (< 100 mots)": "moins de 100 mots",
                "Moyen (100-200 mots)": "entre 100 et 200 mots",
                "Long (200+ mots)": "plus de 200 mots"}
    return f"""
Crée un contenu de communication de type "{type_contenu}" pour un service de santé au travail.
Audience : {cible}
Ton : {ton_map[ton]}
Longueur : {long_map[longueur]}
Sujet : {sujet}
Informations complémentaires : {infos if infos else "Aucune"}

Le contenu doit être directement utilisable, professionnel et adapté au secteur de la santé au travail.
Pour un email, inclure un objet percutant. Pour LinkedIn, utiliser des emojis appropriés.
"""

if st.button("✨ Générer le contenu", type="primary", use_container_width=True):
    if not sujet:
        st.error("⚠️ Veuillez indiquer un sujet principal.")
        st.stop()

    with st.spinner("Création du contenu..."):
        if mode == "🎯 Démo":
            resultat = DEMO_CONTENUS.get(type_contenu, DEMO_CONTENUS["📧 Email de newsletter"])
        else:
            try:
                import openai
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Tu es expert en communication pour un service de santé au travail. Tu crées des contenus engageants, professionnels et adaptés à l'audience."},
                        {"role": "user", "content": build_prompt_comm(type_contenu, cible, ton, longueur, sujet, infos_complementaires)},
                    ],
                    temperature=0.6, max_tokens=800,
                )
                resultat = response.choices[0].message.content
            except Exception as e:
                st.error(f"❌ {str(e)}")
                st.stop()

    st.success("✅ Contenu généré !")
    st.divider()
    st.subheader("📄 Résultat")
    st.markdown(resultat)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    st.download_button("💾 Télécharger (.txt)", data=resultat,
        file_name=f"contenu_comm_{ts}.txt", mime="text/plain", use_container_width=True)

st.divider()
st.caption("📣 Contenu à relire avant envoi. Ne pas mentionner de données personnelles.")
