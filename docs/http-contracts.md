# Contratos HTTP

Este documento define los contratos HTTP de los servicios del proyecto Asistente Accionista.

Para cada endpoint se especifican el método HTTP, la ruta, los campos de entrada y salida, las restricciones de validación y los posibles errores.

El objetivo es establecer una interfaz común que permita desarrollar y probar los componentes de forma independiente.

## Endpoint `/ask`

### Descripción

Permite enviar una pregunta al agente del Asistente Accionista y recibir una respuesta en formato texto.

- **Método:** `POST`
- **Ruta:** `/ask`
- **Content-Type:** `application/json`
- **Formato de respuesta:** `application/json`

### Entrada

El cuerpo de la petición debe ser un objeto JSON con los siguientes campos:

| Campo | Tipo | Obligatorio | Restricciones | Descripción |
|---|---|---|---|---|
| `input` | string | Sí | Entre 1 y 200 caracteres, sin contar espacios exteriores | Pregunta que se desea realizar al agente. |

#### Ejemplo de petición

```json
{
  "input": "¿Cuáles fueron los principales motores del crecimiento de Apple en el tercer trimestre fiscal de 2026?"
}
```

#### Reglas de validación

- El cuerpo debe contener un objeto JSON válido.
- El campo `input` es obligatorio y debe ser una cadena de texto.
- La pregunta no puede estar vacía ni contener únicamente espacios en blanco.
- La longitud máxima de `input` es de 200 caracteres, sin contar los espacios al principio y al final.
- No se admiten campos adicionales en la primera versión del contrato.

### Salida satisfactoria

Si la petición es válida y el agente puede procesarla, el servicio devuelve una respuesta con estado HTTP `200 OK`.

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `output` | string | Sí | Respuesta textual generada por el agente. |

#### Ejemplo de respuesta

```json
{
  "output": "Los principales motores del crecimiento fueron las ventas de productos y servicios, aunque es necesario consultar los resultados oficiales para confirmar los factores específicos del trimestre."
}
```

La respuesta debe corresponder a la pregunta recibida. El agente no debe presentar información no verificada como si fuera un hecho confirmado.

### Errores

Las respuestas de error utilizarán un objeto JSON con el siguiente formato común:

| Campo | Tipo | Obligatorio | Descripción |
|---|---|---|---|
| `error` | string | Sí | Código identificativo del error. |
| `message` | string | Sí | Descripción breve del problema. |

| Estado HTTP | Código de error | Situación |
|---|---|---|
| `400 Bad Request` | `INVALID_REQUEST` | El JSON es inválido, falta `input` o el campo no tiene el tipo esperado. |
| `422 Unprocessable Content` | `INPUT_VALIDATION_ERROR` | La pregunta está vacía o supera los 200 caracteres. |
| `500 Internal Server Error` | `INTERNAL_ERROR` | Se ha producido un error interno inesperado. |
| `503 Service Unavailable` | `AGENT_UNAVAILABLE` | El agente o una dependencia necesaria no está disponible temporalmente. |

#### Ejemplo de error de validación

```json
{
  "error": "INPUT_VALIDATION_ERROR",
  "message": "El campo 'input' no puede superar los 200 caracteres."
}
```

### Consideraciones

- La validación de la petición corresponde al servicio HTTP.
- La generación y el contenido de la respuesta corresponden al agente.
- Los errores no deben incluir credenciales, trazas internas ni información sensible.
- Los códigos y formatos definidos en este documento constituyen el contrato de la primera versión del endpoint.