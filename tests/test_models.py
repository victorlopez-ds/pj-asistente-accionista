
import pytest
from pydantic import ValidationError

from asistente_accionista.models import AskRequest, AskResponse


def test_ask_request_valido():
    modelo = AskRequest(input="¿Cómo evolucionaron las acciones de Apple?")
    assert modelo.input == "¿Cómo evolucionaron las acciones de Apple?"


def test_ask_request_sin_input():
    with pytest.raises(ValidationError):
        AskRequest()


def test_ask_request_vacio():
    with pytest.raises(ValidationError):
        AskRequest(input="")


def test_ask_request_mas_de_200_caracteres():
    with pytest.raises(ValidationError):
        AskRequest(input="A" * 201)


def test_ask_request_elimina_espacios():
    modelo = AskRequest(input="  ¿Cómo cotiza Apple?  ")
    assert modelo.input == "¿Cómo cotiza Apple?"


def test_ask_request_rechaza_campos_extra():
    with pytest.raises(ValidationError):
        AskRequest(input="Pregunta válida", campo_extra="no permitido")


def test_ask_response_valido():
    modelo = AskResponse(output="Las acciones subieron un 5 %.")
    assert modelo.output == "Las acciones subieron un 5 %."


def test_ask_response_sin_output():
    with pytest.raises(ValidationError):
        AskResponse()


def test_ask_response_tipo_incorrecto():
    with pytest.raises(ValidationError):
        AskResponse(output=123)
