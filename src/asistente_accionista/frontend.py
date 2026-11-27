import os

import gradio as gr
import httpx


API_URL = os.getenv(
    "API_URL", "http://127.0.0.1:8000/ask"
)


def ask_assistant(message, history):
    question = message.strip()

    if not question:
        raise gr.Error("Debes introducir una pregunta.")

    try:
        response = httpx.post(
            API_URL,
            json={"input": question},
            timeout=60.0,
        )

        response.raise_for_status()

        data = response.json()
        answer = data["output"]

        if not isinstance(answer, str) or not answer.strip():
            raise ValueError("Respuesta inválida")

        return answer

    except httpx.TimeoutException:
        return (
            "El asistente está tardando demasiado en responder. "
            "Por favor, inténtalo nuevamente."
        )

    except httpx.HTTPStatusError:
        return (
            "La API ha devuelto un error. "
            "Por favor, inténtalo nuevamente."
        )

    except httpx.RequestError:
        return (
            "No se pudo conectar con el asistente. "
            "Comprueba que el servicio esté disponible."
        )

    except (ValueError, KeyError, TypeError):
        return (
            "Se recibió una respuesta inesperada del asistente. "
            "Por favor, inténtalo nuevamente."
        )


def create_frontend():
    return gr.ChatInterface(
        fn=ask_assistant,
        title="Asistente Accionista",
        description=(
            "Asistente de inteligencia artificial para consultar "
            "y analizar información pública de empresas cotizadas. "
            "Esta herramienta no ofrece recomendaciones de inversión."
        ),
        textbox=gr.Textbox(
            placeholder="Escribe tu pregunta...",
            submit_btn=True,
        ),
        examples=[
            "¿Qué es un informe financiero 10-K?",
            "¿Qué información contiene un earnings call?",
            "¿Cómo se interpretan los factores de riesgo?",
        ],
    )
