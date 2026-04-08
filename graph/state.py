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