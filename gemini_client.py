import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    raise ValueError(
        "La clé API OpenRouter est introuvable dans .env"
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1",
    timeout=60.0,
    max_retries=2
)

def ask_llm(question):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=[
            {"role": "user", "content": question}
        ],
        temperature=0.2
    )

    return response.choices[0].message.content

def ask_gemini(question):
    return ask_llm(question)
