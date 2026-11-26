import os
from groq import Groq


def generate_response(question: str) -> str:
    """Genera una respuesta utilizando la API de Groq."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError("GROQ_API_KEY is not configured")

    client = Groq(api_key=api_key, timeout=30.0)

    response = client.chat.completions.create(
        model=os.getenv(
            "GROQ_MODEL", "llama-3.3-70b-versatile"
        ),
        messages=[
            {
                "role": "system",
                "content": (
                    "Eres un asistente especializado en análisis "
                    "financiero y empresas cotizadas. "
                    "Responde en español de forma clara y objetiva. "
                    "No inventes datos financieros. "
                    "Si no dispones de información suficiente, "
                    "indícalo expresamente."
                ),
            },
            {
                "role": "user",
                "content": question,
            },
        ],
        temperature=0.3,
        max_completion_tokens=1024,
    )

    output = response.choices[0].message.content

    if not output or not output.strip():
        raise RuntimeError("Empty response from LLM provider")

    return output.strip()
