# 🎯 Ad Generator App

Application de génération d'affiches publicitaires utilisant LangChain et LangGraph avec l'IA Gemini.

## Fonctionnalités

- Upload d'une image produit
- Analyse automatique du produit par IA
- Génération d'affiche publicitaire professionnelle
- Interface Streamlit moderne

## Architecture

- **Agent 1** : Analyse visuelle du produit et génération de prompt publicitaire
- **Agent 2** : Génération de l'affiche avec Gemini 3.1 Flash Image Preview
- Pipeline LangGraph pour l'orchestration

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/omagbogan/generateur-de-pub.git
cd generateur-de-pub
```

2. Installer les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurer les variables d'environnement :
Créer un fichier `.env` avec :
```
OPENROUTER_API_KEY=votre_clé_api_openrouter
```

4. Lancer l'application :
```bash
streamlit run app.py
```

## Tutoriel pour Débutants

📚 **[TUTORIEL_DEBUTANT.md](TUTORIEL_DEBUTANT.md)** - Guide ultra-détaillé pour créer cette application depuis zéro, même si vous n'avez jamais codé !

Ce tutoriel explique :
- Installation de Python et des outils
- Concepts de base de la programmation
- Création de chaque fichier pas à pas
- Compréhension de l'architecture IA
- Dépannage et débogage
- Publication sur GitHub

## Structure du projet

```
├── app.py                 # Application principale Streamlit
├── requirements.txt       # Dépendances Python
├── .env                   # Variables d'environnement (non commité)
├── agents/
│   ├── agent1_vision.py   # Analyse du produit
│   └── agent2_image_gen.py # Génération d'affiche
├── graph/
│   ├── pipeline.py        # Pipeline LangGraph
│   └── state.py          # État partagé
└── utils/
    └── llm_config.py     # Configuration des LLMs
```

## Utilisation

1. Uploader une image de produit
2. Cliquer sur "Générer l'affiche"
3. L'IA analyse le produit et crée une affiche publicitaire personnalisée

## Licence

MIT License