from fastapi import FastAPI, HTTPException
from groq import APIError

from .models import AskRequest, AskResponse
from .llm_service import generate_response


app = FastAPI(
    title="Asistente IA Accionista",
    version="0.1.0"
)


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    try:
        output = generate_response(request.input)
        return AskResponse(output=output)

    except RuntimeError:
        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable"
        )

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="Error communicating with LLM provider"
        )
