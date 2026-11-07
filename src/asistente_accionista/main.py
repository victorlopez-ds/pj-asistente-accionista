#Importaciones
from fastapi import FastAPI
from .models import AskRequest, AskResponse
 
#App
app = FastAPI(title="Asistente IA Accionista", version="0.1.0") 
@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return AskResponse(output=f"Respuesta a: {request.input}")
