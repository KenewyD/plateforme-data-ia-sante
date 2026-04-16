# 🏥 Plateforme Data & IA – Santé au Travail

> Application web multi-pages développée avec **Python + Streamlit**, couvrant l'ensemble des missions d'un Analyste Data & IA en service de santé au travail : analyse des données adhérents, assistant IA, génération de rapports, communication et conformité RGPD.

## 🚀 Démo en ligne

👉 **[[Accéder à la plateforme](LIEN_STREAMLIT_ICI)](https://plateforme-data-ia-sante-kavh82qk8xx8h3nynatng4.streamlit.app/Conformite_RGPD)**

---

## 📋 Pages & Fonctionnalités

| Page | Description |
|---|---|
| 🏠 **Accueil** | KPI globaux, alertes prioritaires, activité 12 mois |
| 🔍 **Analyse Adhérents** | Scoring de risque de départ, segmentation, export CSV |
| 💬 **Chatbot IA** | Assistant conversationnel métier avec contexte (médecin, RH, direction...) |
| 📋 **Générateur Rapports** | Rapports automatiques exportables (.md / .txt) |
| 📣 **Campagne Communication** | Créateur de contenu IA (emails, posts LinkedIn, annonces) |
| 🛡️ **Conformité RGPD** | Anonymisation de texte, checklist conformité, registre des traitements |

---

## 🛠️ Stack technique

| Outil | Rôle |
|---|---|
| Python 3.8+ | Langage principal |
| Streamlit | Interface web multi-pages |
| Plotly | Visualisations interactives |
| Pandas / NumPy | Traitement des données |
| OpenAI API (GPT-4) | IA générative (chatbot, rapports, contenu) |
| Regex | Détection et anonymisation RGPD |

---

## 🚀 Installation

```bash
git clone https://github.com/KenewyD/plateforme-data-ia-sante.git
cd plateforme-data-ia-sante
pip install -r requirements.txt
streamlit run app.py
```

---

## ⚙️ Mode Démo

Toutes les pages fonctionnent **sans clé API OpenAI** grâce au mode démo intégré. Pour activer l'IA réelle, créez un fichier `.env` avec votre clé :
```
OPENAI_API_KEY=sk-...
```

---

## 📈 Cas d'usage couverts

- ✅ Pilotage de l'activité médicale en temps réel
- ✅ Détection proactive des adhérents à risque de départ
- ✅ Automatisation de la rédaction de rapports
- ✅ Création de contenu de communication ciblé
- ✅ Assistance IA pour les équipes internes
- ✅ Conformité RGPD et anonymisation des données

---

## 👩‍💻 Auteure

**Kenewy Diallo** – Analyste Data & IA
📍 Montpellier | 🔗 [LinkedIn](https://linkedin.com/in/kenewy-diallo)
