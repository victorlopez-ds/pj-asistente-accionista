#Importaciones de Pydantic
from pydantic import BaseModel, ConfigDict, Field, ValidationError

#Así definiremos nuestro AskRequest
class AskRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True, json_schema_extra={"example": {"input": "¿Cuáles fueron los principales motivos del crecimiento de Apple en el tercer trimestre de 2026?"}},)
    input: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Esta es la pregunta que llega a nuestro agente (que tendra que tener como maximo una extensión de 1-200 caracteres, sin contar los espacios exteriores o los vacios).",
    )

#Como es nuestro AskResponse
class AskResponse(BaseModel):
    model_config = ConfigDict(json_schema_extra={"example": {"output": "En el tercer trimestre fiscal de 2026, Apple ingresó 109.417 millones de dólares, un 16,4 % más que los del mismo trimestre del año pasado. Los ingresos del iPhone aumentaron en un 21,7 % y explica por sí solo cerca del 63 % del aumento de ingresos globales. Le siguió el Mac, con 10.352 millones. Otros accesorios crecieron su facturación en un 6,5 % y el iPad cayó un 5,9 %. El margen bruto de la compañia subió del 46,5 % al 50,1 %, y la propia apple ha dicho que unos 2 puntos proceden de devolucion de aranceles; el beneficio por acción fue de 2,02 dólares, 0,11 de ellos por ese mismo concepto.}})
    output: str = Field(
        ..., 
        description="Respuesta final generada por el agente asistente IA accionista"
    )
