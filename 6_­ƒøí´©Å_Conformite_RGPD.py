"""
Page 6 – Conformité RGPD : Anonymisation & vérification
"""
import streamlit as st
import re
import pandas as pd

st.set_page_config(page_title="Conformité RGPD", page_icon="🛡️", layout="centered")
st.title("🛡️ Outil de Conformité RGPD")
st.markdown("*Anonymisez vos textes et vérifiez la conformité de vos documents avant diffusion.*")
st.divider()

# ── Onglets ───────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["🔍 Détection & Anonymisation", "✅ Checklist RGPD", "📊 Registre des traitements"])

# ── Tab 1 : Anonymisation ─────────────────────────────────────────────────────
with tab1:
    st.subheader("🔍 Détection des données personnelles")
    st.info("Collez votre texte ci-dessous. L'outil détecte et anonymise automatiquement les données personnelles.")

    texte_input = st.text_area("📝 Texte à analyser", height=200,
        placeholder="Ex : Le salarié Jean Dupont, né le 12/03/1985, domicilié au 15 rue de la Paix, 75001 Paris, tél. 06.12.34.56.78, email : jean.dupont@email.com...")

    PATTERNS = {
        "Email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "Téléphone": r'\b(0|\+33)[1-9]([-. ]?\d{2}){4}\b',
        "Date naissance": r'\b\d{2}[/.-]\d{2}[/.-]\d{4}\b',
        "Numéro SS": r'\b[12]\s?\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\s?\d{3}\s?\d{2}\b',
        "Code postal": r'\b\d{5}\b',
    }

    NOMS_COMMUNS = ["dupont","martin","bernard","thomas","petit","robert","richard",
                    "durand","moreau","simon","marie","jean","pierre","paul","sophie"]

    if st.button("🔍 Analyser et anonymiser", type="primary", use_container_width=True):
        if not texte_input:
            st.error("Veuillez entrer un texte.")
        else:
            texte_anonymise = texte_input
            detections = []

            for type_donnee, pattern in PATTERNS.items():
                matches = re.findall(pattern, texte_anonymise, re.IGNORECASE)
                if matches:
                    for match in matches:
                        detections.append({"Type": type_donnee, "Valeur détectée": match, "Action": "✅ Anonymisé"})
                    remplacement = {
                        "Email": "[EMAIL]",
                        "Téléphone": "[TÉLÉPHONE]",
                        "Date naissance": "[DATE]",
                        "Numéro SS": "[N°SS]",
                        "Code postal": "[CP]",
                    }[type_donnee]
                    texte_anonymise = re.sub(pattern, remplacement, texte_anonymise, flags=re.IGNORECASE)

            # Noms propres (heuristique simple)
            mots = texte_anonymise.split()
            for i, mot in enumerate(mots):
                mot_clean = re.sub(r'[^a-zA-ZÀ-ÿ]', '', mot).lower()
                if mot_clean in NOMS_COMMUNS or (len(mot_clean) > 3 and mot[0].isupper() and i > 0):
                    detections.append({"Type": "Nom propre (probable)", "Valeur détectée": mot, "Action": "⚠️ À vérifier"})
                    mots[i] = "[NOM]"
            texte_anonymise = " ".join(mots)

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("⚠️ Données détectées")
                if detections:
                    st.dataframe(pd.DataFrame(detections), use_container_width=True, hide_index=True)
                else:
                    st.success("✅ Aucune donnée personnelle détectée.")

            with col2:
                st.subheader("✅ Texte anonymisé")
                st.text_area("Résultat", texte_anonymise, height=200)
                st.download_button("💾 Télécharger le texte anonymisé",
                    data=texte_anonymise, file_name="texte_anonymise.txt", mime="text/plain",
                    use_container_width=True)

# ── Tab 2 : Checklist RGPD ───────────────────────────────────────────────────
with tab2:
    st.subheader("✅ Checklist de conformité RGPD – Santé au Travail")

    categories = {
        "📋 Bases légales": [
            "La base légale du traitement est définie (obligation légale, intérêt légitime...)",
            "Le registre des traitements est à jour",
            "Les finalités de traitement sont clairement définies",
        ],
        "🔒 Sécurité des données": [
            "Les données de santé sont chiffrées au repos et en transit",
            "Les accès sont restreints aux personnes habilitées",
            "Une politique de mots de passe est en place",
            "Les sauvegardes sont régulières et testées",
        ],
        "👤 Droits des personnes": [
            "Les personnes sont informées du traitement de leurs données",
            "Le droit d'accès est facilement exercisable",
            "Le droit à l'effacement est opérationnel",
            "Les demandes de droits sont traitées sous 30 jours",
        ],
        "⏰ Conservation des données": [
            "Les durées de conservation sont définies par type de données",
            "Les données médicales sont conservées 50 ans (dossier médical en santé travail)",
            "Un processus de purge automatique est en place",
        ],
        "🤝 Sous-traitants": [
            "Les contrats de sous-traitance incluent des clauses RGPD",
            "Les transferts hors UE sont encadrés",
            "Le DPO est informé de tout nouveau sous-traitant",
        ],
    }

    score_total = 0
    score_max = 0

    for categorie, items in categories.items():
        st.markdown(f"**{categorie}**")
        for item in items:
            score_max += 1
            checked = st.checkbox(item, key=f"check_{item}")
            if checked:
                score_total += 1

    st.divider()
    score_pct = int(score_total / score_max * 100)
    couleur = "🟢" if score_pct >= 80 else "🟡" if score_pct >= 50 else "🔴"
    st.metric(f"{couleur} Score de conformité", f"{score_pct}%", f"{score_total}/{score_max} critères validés")
    st.progress(score_pct / 100)

# ── Tab 3 : Registre ─────────────────────────────────────────────────────────
with tab3:
    st.subheader("📊 Registre des traitements de données")
    st.info("Exemple de registre des traitements pour un service de santé au travail.")

    registre = pd.DataFrame({
        "Traitement": ["Dossiers médicaux", "Gestion adhérents", "Communication", "Facturation", "Vidéosurveillance"],
        "Finalité": ["Suivi médical salarié", "Gestion contractuelle", "Newsletters & info", "Gestion financière", "Sécurité locaux"],
        "Base légale": ["Obligation légale", "Contrat", "Consentement", "Obligation légale", "Intérêt légitime"],
        "Données sensibles": ["✅ Oui", "❌ Non", "❌ Non", "❌ Non", "⚠️ Biométriques"],
        "Conservation": ["50 ans", "5 ans", "3 ans", "10 ans", "30 jours"],
        "Responsable": ["Médecin DT", "Direction", "Communication", "Comptabilité", "Direction"],
    })
    st.dataframe(registre, use_container_width=True, hide_index=True)

    csv = registre.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Exporter le registre (.csv)", data=csv,
        file_name="registre_traitements_rgpd.csv", mime="text/csv", use_container_width=True)

st.divider()
st.caption("🛡️ Cet outil est un aide à la conformité. Consultez votre DPO pour validation.")
