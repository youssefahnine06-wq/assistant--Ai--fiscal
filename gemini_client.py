import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("La clé API Gemini est introuvable dans le fichier .env")

client = genai.Client(api_key=API_KEY)


def ask_gemini(question):
    response = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=question
    )

    return response.text
