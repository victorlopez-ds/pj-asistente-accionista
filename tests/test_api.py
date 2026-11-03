from fastapi.testclient import TestClient
from asistente_accionista.main import app

client = TestClient(app)


def test_ask_respuesta_correcta():
    response = client.post(
        "/ask",
        json={
            "input": "¿Cuáles fueron los principales motivos del crecimiento de Apple?"
        }
    )

    assert response.status_code == 200
    assert "output" in response.json()
    assert isinstance(response.json()["output"], str)