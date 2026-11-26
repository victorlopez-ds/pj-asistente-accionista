from unittest.mock import patch

import httpx
from groq import APIConnectionError
from fastapi.testclient import TestClient
from asistente_accionista.main import app


client = TestClient(app)


@patch("asistente_accionista.main.generate_response")
def test_ask_respuesta_correcta(mock_generate):
    mock_generate.return_value = "Respuesta generada por IA."

    pregunta = "¿Cómo evolucionaron las acciones de Apple?"

    response = client.post(
        "/ask",
        json={"input": pregunta}
    )

    assert response.status_code == 200
    assert response.json()["output"] == "Respuesta generada por IA."
    mock_generate.assert_called_once_with(pregunta)


@patch("asistente_accionista.main.generate_response")
def test_ask_servicio_no_disponible(mock_generate):
    mock_generate.side_effect = RuntimeError("Service unavailable")

    response = client.post(
        "/ask",
        json={"input": "¿Cómo cotiza Apple?"}
    )

    assert response.status_code == 503


@patch("asistente_accionista.main.generate_response")
def test_ask_error_proveedor(mock_generate):
    mock_generate.side_effect = APIConnectionError(
        request=httpx.Request("POST", "https://api.groq.com")
    )

    response = client.post(
        "/ask",
        json={"input": "¿Cómo cotiza Apple?"}
    )

    assert response.status_code == 502


@patch("asistente_accionista.main.generate_response")
def test_ask_input_invalido(mock_generate):
    response = client.post(
        "/ask",
        json={"input": ""}
    )

    assert response.status_code == 422
    mock_generate.assert_not_called()
