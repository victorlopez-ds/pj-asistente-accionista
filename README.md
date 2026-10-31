# Asistente Accionista

## Descripción

Asistente conversacional basado en inteligencia artificial generativa que ayuda a inversores particulares a consultar y analizar información pública de empresas cotizadas mediante lenguaje natural. El sistema utiliza documentación corporativa, como informes anuales (10-K) y transcripciones de presentaciones de resultados (*earnings calls*), para localizar y sintetizar información relevante.

Es una herramienta de apoyo al análisis, no un asesor financiero: no ofrece recomendaciones de inversión.

## Estructura del proyecto
```text
pj-asistente-accionista/
├── .github/
│   └── workflows/
│       └── test_and_build.yml
├── data/
├── deployment/
│   └── Dockerfile
├── docs/
│   └── http-contracts.md
├── src/
│   └── asistente_accionista/
│       ├── __init__.py
│       ├── main.py
│       └── models.py
├── tests/
│   ├── test_api.py
│   └── test_models.py
├── requirements.txt
└── README.md
```

## Código de la aplicación

- El paquete de la aplicación estará en `src/asistente_accionista/`.
- `models.py` contendrá los modelos de Pydantic, incluidos `AskRequest` y `AskResponse`.
- `main.py` contendrá la aplicación FastAPI y el endpoint `POST /ask`.
- `__init__.py` permitirá importar el código como el paquete `asistente_accionista`.

## Tests

- `tests/test_models.py` contendrá los tests unitarios de los modelos Pydantic.
- `tests/test_api.py` contendrá los tests de integración del endpoint usando `TestClient` de FastAPI.
- HTTPX debe estar incluido entre las dependencias necesarias para usar `TestClient`.
- La suite se ejecutará desde la raíz del proyecto con:

  ```bash
  python -m pytest tests/
  ```

## Dependencias

`requirements.txt`, en la raíz, contendrá las dependencias necesarias para la aplicación y para ejecutar los tests. El workflow ya lo instala desde esa ubicación.

## Docker

- El Dockerfile estará en `deployment/Dockerfile`.
- Como la aplicación vive en `src/` y las dependencias en la raíz, el contexto de construcción de Docker debe ser la raíz del repositorio (`.`). El workflow debe apuntar al Dockerfile con la ruta `deployment/Dockerfile`.

## Puesta en marcha en local

## Funcionalidades previstas

- **Consulta de documentación en lenguaje natural:** permite realizar preguntas sobre la información disponible de una empresa mediante un asistente conversacional basado en RAG.
- **Respuestas con fuentes:** identifica los documentos y las fechas que respaldan la información proporcionada para que el usuario pueda consultar su origen.
- **Análisis de información a lo largo del tiempo:** facilita comparar distintos períodos e identificar cambios en los riesgos, las perspectivas y el discurso de la dirección de una empresa.
- **Contraste histórico con la cotización:** permite relacionar retrospectivamente determinadas afirmaciones o cambios de discurso con la evolución histórica de la cotización, con un propósito descriptivo y no predictivo.
- **Análisis cuantitativo experimental:** se plantea explorar modelos de aprendizaje automático para obtener estimaciones probabilísticas sobre series históricas de mercado, incluyendo incertidumbre y riesgo.
- **Preguntas de seguimiento:** funcionalidad avanzada prevista para mantener el contexto de la conversación y profundizar progresivamente en una empresa o cuestión.
- **Comparativa entre empresas:** funcionalidad avanzada planteada para facilitar el análisis comparativo de distintas compañías.
