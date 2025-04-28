# Analyse de Sentiment Financier 📈

[![Hugging Face](https://img.shields.io/badge/HuggingFace-Model-yellow?logo=huggingface)](https://huggingface.co/mrm8488/distilroberta-finetuned-financial-news-sentiment-analysis)
[![Gradio App](https://img.shields.io/badge/Made%20with-Gradio-ff6e00?logo=gradio)](https://gradio.app/)

Application web simple pour analyser le **sentiment** de textes liés aux **actualités financières**, en utilisant un modèle NLP pré-entraîné.

---

## 🧭 Sommaire

- [Objectif](#objectif)
- [Technologies utilisées](#technologies-utilisées)
- [Installation](#installation)
- [Utilisation](#utilisation)
- [Fonctionnalités](#fonctionnalités)
- [Aperçu](#aperçu)
- [Améliorations futures](#améliorations-futures)
- [Licence](#licence)

---

## 🎯 Objectif

Entrer une phrase liée aux finances ou à l'économie, et obtenir :
- L'**analyse du sentiment** (positif, négatif, neutre),
- Un **score de confiance**,
- Un **graphique en camembert** généré automatiquement.

---

## 🛠️ Technologies utilisées

- 🤗 **Transformers** (Hugging Face) pour l'IA NLP
- 🎨 **Matplotlib** pour les graphiques
- 🚀 **Gradio** pour créer l'application web
- 🔥 **PyTorch** pour le backend du modèle

---

## 📦 Installation

Clonez le projet et installez les dépendances :

```bash
git clone <URL_DU_REPO>
cd <nom_du_dossier>
pip install -r requirements.txt
```

Exemple de `requirements.txt` :
```
transformers
gradio
matplotlib
torch
```

---

## 🚀 Utilisation

Lancez l'application en local :

```bash
python app.py
```

Puis ouvrez votre navigateur à l'adresse :  
`http://127.0.0.1:7860/`

---

## ✨ Fonctionnalités

- Analyse de sentiments financiers rapide.
- Retour du **sentiment** et du **score** dans l'interface.
- Graphique circulaire interactif.
- Gestion des erreurs (texte vide).
- Interface épurée et responsive.

---

## 📸 Aperçu

Voici un aperçu de l'application en action :  

![Demo de l'App](assets/results.png)

---

## 🔥 Améliorations futures

- Support multilingue.
- Sélection dynamique de modèles (choisir un modèle dans une liste déroulante).
- Télécharger des rapports d'analyse.
- Mode "dark" pour l'interface.

---

## 📜 Licence

Projet open-source réalisé pour m'entraîner à l'IA, aux interfaces web, et au NLP.  
N'hésitez pas à proposer des améliorations ou à forker !

---