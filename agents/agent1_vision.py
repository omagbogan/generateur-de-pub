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
            "text": """Tu es un expert en marketing et publicité visuelle avec plus de 20 ans d'expérience dans la création d'affiches publicitaires à succès.
Analyse ce produit en détail et génère un prompt extrêmement détaillé et professionnel en anglais pour créer une affiche publicitaire exceptionnelle qui se démarque.

Le prompt doit être complet et inclure :

**Analyse du produit :**
- Description détaillée du produit, ses caractéristiques uniques, matériaux, fonctionnalités
- Positionnement marketing (luxe, abordable, écologique, technologique, etc.)
- Public cible idéal (âge, genre, style de vie, valeurs)

**Style visuel avancé :**
- Mouvement artistique spécifique (photographie réaliste, illustration stylisée, 3D rendu, minimalisme extrême, art abstrait, etc.)
- Palette de couleurs sophistiquée avec codes hexadécimaux si pertinent
- Typographie précise (familles de polices, tailles, poids, hiérarchie)
- Composition artistique (règles des tiers, golden ratio, asymétrie dynamique)

**Ambiance et storytelling :**
- Atmosphère émotionnelle (inspiration, confiance, excitation, sérénité, urgence)
- Scénario narratif complet (contexte d'utilisation, histoire derrière le produit)
- Inclusion d'une personne représentative tenant le produit en main (démographie adaptée au public cible, expression faciale engageante, pose naturelle)
- Éclairage professionnel (direction, intensité, ombres dramatiques, reflets)

**Éléments publicitaires stratégiques :**
- Slogans accrocheurs et mémorables
- Call-to-action clair et persuasif
- Éléments de preuve sociale ou de confiance (certifications, témoignages)
- Intégration subtile de branding

**Détails techniques :**
- Résolution et format optimaux
- Aspect ratio spécifique (9:16 pour mobile, 16:9 pour web, etc.)
- Qualité d'impression envisagée
- Adaptabilité cross-platform

**Innovation créative :**
- Twist unique ou concept original
- Métaphores visuelles puissantes
- Symbolisme culturellement adapté
- Tendances actuelles intégrées

Le prompt doit être écrit comme une directive professionnelle complète pour un designer graphique expert, avec un langage précis et inspirant qui garantit une affiche visuellement époustouflante et commercialement efficace.

Réponds UNIQUEMENT avec le prompt généré, sans introduction ni explication."""
        }
    ])

    response = llm.invoke([message])
    
    return {"ad_prompt": response.content}