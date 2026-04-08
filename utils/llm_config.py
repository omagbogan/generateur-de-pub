import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

def get_vision_llm():
    """Agent 1 — analyse image, génère prompt publicitaire"""
    return ChatOpenAI(
        model="google/gemini-2.0-flash-001",  # ✅ Remplace gemini-flash-1.5
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