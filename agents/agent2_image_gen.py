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

    # 🔍 DEBUG — affiche la structure complète de la réponse
    print("=== REPONSE API BRUTE ===")
    print(json.dumps(data, indent=2))
    print("========================")

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