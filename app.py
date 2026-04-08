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

            with st.expander("📝 Prompt publicitaire généré (Agent 1)"):
                st.write(result["ad_prompt"])

            # Bouton de téléchargement
            st.download_button(
                label="⬇️ Télécharger l'affiche",
                data=base64.b64decode(result["generated_image_b64"]),
                file_name="affiche_publicitaire.png",
                mime="image/png"
            )