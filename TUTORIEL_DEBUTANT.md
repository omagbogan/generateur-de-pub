# 🚀 Tutoriel Complet : Créer un Générateur d'Affiches Publicitaires IA

## Pour les Débutants en Programmation

Ce tutoriel vous guide pas à pas pour créer votre propre application de génération d'affiches publicitaires utilisant l'Intelligence Artificielle. Pas besoin d'être un expert - suivez simplement les étapes !

---

## 📋 Prérequis (Ce dont vous avez besoin avant de commencer)

### 1. Comprendre les Bases
Avant de commencer, vous devez savoir :
- **Qu'est-ce qu'un programme ?** Un ensemble d'instructions que l'ordinateur exécute
- **Qu'est-ce que Python ?** Un langage de programmation simple et puissant
- **Qu'est-ce qu'une API ?** Une interface qui permet à votre programme de communiquer avec des services externes (comme l'IA)

### 2. Installer Python
Python est le langage que nous allons utiliser.

**Windows :**
1. Allez sur https://www.python.org/downloads/
2. Téléchargez la version 3.11 ou plus récente
3. Lors de l'installation, **cochez "Add Python to PATH"**
4. Vérifiez l'installation : ouvrez l'invite de commande et tapez `python --version`

**Mac :**
```bash
# Avec Homebrew (recommandé)
brew install python

# Ou téléchargez depuis python.org
```

**Linux :**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 3. Comprendre les Concepts Clés
Avant de coder, apprenons les concepts :

#### Variables
```python
nom = "Alice"  # Stocke du texte
age = 25       # Stocke un nombre
est_actif = True  # Stocke vrai/faux
```

#### Fonctions
```python
def saluer(nom):
    return f"Bonjour {nom} !"

message = saluer("Alice")  # message = "Bonjour Alice !"
```

#### Modules/Bibliothèques
Des "boîtes à outils" que d'autres ont créées :
- `streamlit` : pour créer des applications web
- `langchain` : pour travailler avec l'IA
- `PIL` : pour manipuler les images

---

## 🏗️ Étape 1 : Créer la Structure du Projet

### 1.1 Créer le Dossier du Projet
```bash
# Créez un dossier pour votre projet
mkdir generateur-affiches-ia
cd generateur-affiches-ia
```

### 1.2 Créer la Structure des Dossiers
```
generateur-affiches-ia/
├── app.py                    # L'application principale
├── requirements.txt          # Liste des bibliothèques nécessaires
├── .env                      # Clés secrètes (ne pas partager)
├── README.md                 # Documentation
├── .gitignore               # Fichiers à ignorer
├── agents/                   # Dossier pour les agents IA
│   ├── agent1_vision.py      # Agent qui analyse les images
│   └── agent2_image_gen.py   # Agent qui génère les affiches
├── graph/                    # Logique de l'application
│   ├── pipeline.py           # Orchestration des agents
│   └── state.py              # Données partagées
└── utils/                    # Outils utilitaires
    └── llm_config.py         # Configuration de l'IA
```

**Pourquoi cette structure ?**
- `agents/` : Chaque agent IA a sa propre responsabilité
- `graph/` : La logique de coordination entre agents
- `utils/` : Code réutilisable

---

## 📦 Étape 2 : Installer les Outils Nécessaires

### 2.1 Créer l'Environnement Virtuel
Un environnement virtuel isole votre projet des autres projets Python.

```bash
# Créer l'environnement
python -m venv env

# Activer l'environnement
# Windows :
env\Scripts\activate
# Mac/Linux :
source env/bin/activate

# Vous verrez (env) au début de votre ligne de commande
```

### 2.2 Installer les Bibliothèques
Créez le fichier `requirements.txt` :

```txt
streamlit>=1.28.0
langchain>=0.1.0
langchain-openai>=0.0.8
langgraph>=0.0.40
python-dotenv>=1.0.0
Pillow>=10.0.0
httpx>=0.25.0
```

Installez-les :
```bash
pip install -r requirements.txt
```

**Que fait chaque bibliothèque ?**
- `streamlit` : Interface web facile à créer
- `langchain` : Framework pour l'IA
- `langgraph` : Coordination d'agents IA
- `python-dotenv` : Gestion des secrets
- `Pillow` : Traitement d'images
- `httpx` : Requêtes HTTP modernes

---

## 🔑 Étape 3 : Obtenir les Clés API

### 3.1 Comprendre les APIs
Les APIs sont comme des services externes. Ici, nous utilisons OpenRouter pour accéder à des modèles d'IA.

### 3.2 Créer un Compte OpenRouter
1. Allez sur https://openrouter.ai/
2. Créez un compte gratuit
3. Allez dans "Keys" pour créer une clé API
4. Copiez la clé (elle commence par `sk-or-v1-`)

### 3.3 Créer le Fichier .env
```bash
# Créez le fichier .env
touch .env
```

Contenu du fichier `.env` :
```
OPENROUTER_API_KEY=sk-or-v1-votre-cle-api-ici
```

**⚠️ IMPORTANT :**
- Ne partagez JAMAIS ce fichier
- Il contient vos clés secrètes

---

## 🎯 Étape 4 : Comprendre l'Architecture de l'Application

### 4.1 Le Flux de l'Application
```
1. Utilisateur upload une image produit
2. Agent 1 analyse l'image et crée un prompt détaillé
3. Agent 2 utilise le prompt pour générer une affiche
4. Affichage du résultat
```

### 4.2 Les Agents IA
**Agent 1 (Vision) :**
- Reçoit : Image du produit
- Fait : Analyse détaillée du produit
- Produit : Prompt textuel pour l'affiche

**Agent 2 (Génération) :**
- Reçoit : Prompt de l'Agent 1
- Fait : Génère l'image de l'affiche
- Produit : Image base64 de l'affiche

### 4.3 État Partagé (State)
L'état contient toutes les données qui circulent entre les agents :
```python
{
    "image_base64": "...",        # Image uploadée
    "image_mime_type": "image/jpeg",
    "ad_prompt": "...",           # Prompt généré par Agent 1
    "generated_image_b64": "...", # Affiche finale
    "error": None                 # Messages d'erreur
}
```

---

## 💻 Étape 5 : Coder l'Application (Fichier par Fichier)

### 5.1 Créer le Fichier d'État (`graph/state.py`)

```python
from typing import TypedDict, Optional

class AdState(TypedDict):
    # --- Entrée utilisateur ---
    image_base64: str        # Image produit encodée en base64
    image_mime_type: str     # ex: "image/jpeg" ou "image/png"

    # --- Sortie Agent 1 ---
    ad_prompt: Optional[str] # Prompt publicitaire généré par l'Agent 1

    # --- Sortie Agent 2 ---
    generated_image_b64: Optional[str]  # Affiche générée en base64
    error: Optional[str]                # Message d'erreur si problème
```

**Explication :**
- `TypedDict` : Définit la structure des données
- `Optional` : Le champ peut être None au début

### 5.2 Configuration de l'IA (`utils/llm_config.py`)

```python
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_vision_llm():
    """Agent 1 — analyse image, génère prompt publicitaire"""
    return ChatOpenAI(
        model="google/gemini-2.0-flash-001",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=1024,
    )

def get_image_gen_llm():
    """Agent 2 — génère l'affiche via Gemini 2.5 Flash Image"""
    return ChatOpenAI(
        model="google/gemini-2.5-flash-image",
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        max_tokens=1024,
    )
```

**Explication :**
- `load_dotenv()` : Charge les variables du fichier .env
- `os.getenv()` : Récupère la valeur de la variable d'environnement
- Deux fonctions pour deux types d'IA différents

### 5.3 Agent 1 : Analyse de l'Image (`agents/agent1_vision.py`)

```python
from langchain_core.messages import HumanMessage
from utils.llm_config import get_vision_llm
from graph.state import AdState

def agent1_analyze(state: AdState) -> dict:
    """
    Reçoit l'image du produit, retourne un prompt
    détaillé pour générer une affiche publicitaire.
    """
    llm = get_vision_llm()

    message = HumanMessage(content=[
        {
            "type": "image_url",
            "image_url": {
                "url": f"data:{state['image_mime_type']};base64,{state['image_base64']}"
            }
        },
        {
            "type": "text",
            "text": """Tu es un expert en marketing et publicité visuelle.
Analyse ce produit en détail et génère un prompt en anglais
pour créer une affiche publicitaire professionnelle.

Le prompt doit décrire :
- Le style visuel (moderne, luxe, minimaliste, etc.)
- L'ambiance et les couleurs dominantes
- Le placement du produit dans la scène
- Le texte ou slogan suggéré
- L'éclairage et la composition

Réponds UNIQUEMENT avec le prompt, sans introduction ni explication."""
        }
    ])

    response = llm.invoke([message])
    
    return {"ad_prompt": response.content}
```

**Explication :**
- `HumanMessage` : Format pour envoyer du contenu à l'IA
- Contenu mixte : image + texte d'instruction
- L'IA analyse l'image et génère un prompt détaillé

### 5.4 Agent 2 : Génération d'Affiche (`agents/agent2_image_gen.py`)

```python
import httpx
import base64
import json
import os
from graph.state import AdState

def agent2_generate(state: AdState) -> dict:
    prompt = state["ad_prompt"]
    image_b64 = state["image_base64"]
    mime_type = state["image_mime_type"]

    payload = {
        "model": "google/gemini-3.1-flash-image-preview",
        "modalities": ["image", "text"],
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{image_b64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": f"Using this product image as reference, generate a professional advertising poster. {prompt}"
                    }
                ]
            }
        ]
    }

    response = httpx.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
            "Content-Type": "application/json"
        },
        json=payload,
        timeout=120.0
    )

    if response.status_code != 200:
        print(f"Erreur API: {response.status_code}")
        print(f"Réponse: {response.text}")
        return {"generated_image_b64": None, "error": f"Erreur API: {response.status_code}"}

    data = response.json()

    # Extraire l'image
    message = data["choices"][0]["message"]
    if "images" in message and message["images"]:
        image_data_url = message["images"][0]["image_url"]["url"]
        # Extraire le base64 de data:image/png;base64,...
        if image_data_url.startswith("data:image/"):
            generated_image_b64 = image_data_url.split(",")[1]
        else:
            # Si c'est une URL, télécharger
            img_response = httpx.get(image_data_url)
            generated_image_b64 = base64.b64encode(img_response.content).decode("utf-8")
        return {"generated_image_b64": generated_image_b64}
    else:
        return {"generated_image_b64": None, "error": "Aucune image générée"}
```

**Explication :**
- Utilise l'API OpenRouter directement
- Envoie le prompt et l'image de référence
- Reçoit une image générée en base64

### 5.5 Pipeline d'Orchestration (`graph/pipeline.py`)

```python
from langgraph.graph import StateGraph, END
from graph.state import AdState
from agents.agent1_vision import agent1_analyze
from agents.agent2_image_gen import agent2_generate

def build_graph():
    graph = StateGraph(AdState)

    # Ajouter les noeuds
    graph.add_node("agent1_vision", agent1_analyze)
    graph.add_node("agent2_image_gen", agent2_generate)

    # Définir le flux
    graph.set_entry_point("agent1_vision")
    graph.add_edge("agent1_vision", "agent2_image_gen")
    graph.add_edge("agent2_image_gen", END)

    return graph.compile()

# Instance globale réutilisable
ad_pipeline = build_graph()
```

**Explication :**
- `StateGraph` : Définit le workflow
- `add_node` : Ajoute les fonctions agents
- `set_entry_point` : Définit le point de départ
- `add_edge` : Définit les connexions entre agents

### 5.6 Application Principale (`app.py`)

```python
import streamlit as st
import base64
from PIL import Image
import io
from graph.pipeline import ad_pipeline

st.set_page_config(page_title="Ad Generator", layout="centered")
st.title("🎯 Générateur d'affiches publicitaires")
st.caption("Upload une image produit → l'IA génère votre affiche")

uploaded_file = st.file_uploader(
    "Uploade l'image de ton produit",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file:
    # Afficher l'image uploadée
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Image produit")
        st.image(uploaded_file, width="stretch")

    if st.button("✨ Générer l'affiche", type="primary"):
        # Encoder l'image en base64
        image_bytes = uploaded_file.read()
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")
        mime_type = uploaded_file.type  # ex: "image/jpeg"

        # Lancer le pipeline
        with st.spinner("Agent 1 : analyse du produit..."):
            state = {
                "image_base64": image_b64,
                "image_mime_type": mime_type,
                "ad_prompt": None,
                "generated_image_b64": None,
                "error": None,
            }

        with st.spinner("Agent 2 : génération de l'affiche..."):
            result = ad_pipeline.invoke(state)

        # Afficher les résultats
        if result.get("error"):
            st.error(f"Erreur : {result['error']}")
        else:
            with col2:
                st.subheader("Affiche générée")
                img_bytes = base64.b64decode(result["generated_image_b64"])
                st.image(img_bytes, width="stretch")
```

**Explication :**
- Interface utilisateur avec Streamlit
- Upload de fichier
- Conversion en base64
- Exécution du pipeline
- Affichage des résultats

---

## 🧪 Étape 6 : Tester l'Application

### 6.1 Lancer l'Application
```bash
# Assurez-vous que l'environnement virtuel est activé
streamlit run app.py
```

### 6.2 Dépannage Courant

**Erreur "Module not found" :**
```bash
pip install -r requirements.txt
```

**Erreur API :**
- Vérifiez votre clé dans `.env`
- Vérifiez votre connexion internet

**Erreur Image :**
- Vérifiez que l'image uploadée n'est pas trop grande
- Formats supportés : JPG, PNG, WebP

### 6.3 Comprendre les Logs
Quand vous lancez l'app, regardez le terminal :
- Messages de chargement
- Erreurs éventuelles
- Temps de réponse des APIs

---

## 📤 Étape 7 : Publier sur GitHub

### 7.1 Initialiser Git
```bash
git init
git add .
git commit -m "Initial commit: Ad Generator app"
```

### 7.2 Créer le Repository GitHub
1. Allez sur https://github.com/new
2. Créez un repository public
3. Copiez l'URL

### 7.3 Pousser le Code
```bash
git remote add origin https://github.com/votre-username/votre-repo.git
git branch -M main
git push -u origin main
```

---

## 🎓 Concepts Appris

Dans ce tutoriel, vous avez appris :

### Programmation Python
- Variables et types de données
- Fonctions et modules
- Gestion d'erreurs

### Intelligence Artificielle
- APIs et clés d'authentification
- Modèles de vision et génération d'images
- Prompt engineering

### Architecture Logicielle
- Séparation des responsabilités (agents)
- État partagé
- Pipeline d'orchestration

### Développement Web
- Interfaces utilisateur avec Streamlit
- Upload de fichiers
- Affichage d'images

### Outils de Développement
- Environnements virtuels
- Gestion des dépendances
- Contrôle de version (Git)
- Publication sur GitHub

---

## 🚀 Prochaines Étapes

Maintenant que vous avez créé votre première app IA :

1. **Personnalisez** : Changez les prompts, ajoutez des fonctionnalités
2. **Améliorez** : Ajoutez de la validation, gestion d'erreurs
3. **Étendez** : Intégrez d'autres APIs, ajoutez des templates
4. **Partagez** : Montrez votre projet à la communauté

**Rappelez-vous :** Tout le monde commence quelque part. Vous venez de créer une application complète avec de l'IA ! 🎉

---

## 📚 Ressources Supplémentaires

- [Documentation Python](https://docs.python.org/3/)
- [Tutoriels Streamlit](https://docs.streamlit.io/)
- [Guide LangChain](https://python.langchain.com/)
- [OpenRouter Docs](https://openrouter.ai/docs)
- [GitHub pour Débutants](https://guides.github.com/)

**Besoin d'aide ?** N'hésitez pas à poser des questions dans les commentaires du repository !</content>
<parameter name="filePath">c:\Users\obed2\Desktop\MasterClass Langchain et Langraph\TUTORIEL_DEBUTANT.md