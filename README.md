# Asistente Accionista

## Descripción

Asistente conversacional basado en inteligencia artificial generativa que ayuda a inversores particulares a consultar y analizar información pública de empresas cotizadas mediante lenguaje natural. El sistema está diseñado para utilizar documentación corporativa, como informes anuales (10-K) y transcripciones de presentaciones de resultados (*earnings calls*), para localizar y sintetizar información relevante.

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
│       ├── models.py
│       └── llm_service.py
├── tests/
│   ├── test_api.py
│   └── test_models.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Código de la aplicación

- El paquete de la aplicación está en `src/asistente_accionista/`.
- `models.py` contiene los modelos de Pydantic, incluidos `AskRequest` y `AskResponse`.
- `main.py` contiene la aplicación FastAPI y el endpoint `POST /ask`.
- `llm_service.py` gestiona la comunicación con el proveedor LLM Groq y la generación de respuestas.
- `__init__.py` permite importar el código como el paquete `asistente_accionista`.

## Integración con el proveedor LLM

El asistente utiliza la API de Groq para generar respuestas mediante un modelo de lenguaje.

El modelo predeterminado es `openai/gpt-oss-120b` y puede configurarse mediante la variable de entorno `GROQ_MODEL`.

El endpoint `POST /ask` recibe una pregunta, valida los datos mediante Pydantic, solicita una respuesta al proveedor LLM y devuelve el resultado en formato JSON.

La integración contempla:

- Generación dinámica de respuestas mediante inteligencia artificial.
- Separación entre la lógica de la API y la comunicación con el proveedor LLM.
- Configuración segura de credenciales mediante variables de entorno.
- Gestión de errores del proveedor.
- Tests automatizados mediante simulación del servicio LLM.

En esta fase, las respuestas generadas por el LLM todavía no están fundamentadas mediante el sistema RAG previsto. El modelo puede proporcionar información incorrecta o desactualizada.

## Tests

- `tests/test_models.py` contiene los tests unitarios de los modelos Pydantic.
- `tests/test_api.py` contiene los tests de integración del endpoint usando `TestClient` de FastAPI.
- HTTPX está incluido entre las dependencias necesarias para usar `TestClient`.
- Las llamadas al proveedor LLM se simulan mediante mocks, evitando consumir recursos externos o requerir credenciales durante los tests.

La suite se ejecuta desde la raíz del proyecto.

Linux/macOS:

```bash
PYTHONPATH=src python -m pytest tests/ -v
```

Windows PowerShell:

```powershell
$env:PYTHONPATH = "src"
python -m pytest tests/ -v
```

## Dependencias

`requirements.txt`, en la raíz, contiene las dependencias necesarias para la aplicación y para ejecutar los tests. El workflow las instala desde esa ubicación.

Las principales dependencias son:

- FastAPI
- Uvicorn
- Pydantic
- Pytest
- HTTPX
- Groq

## Docker

- El Dockerfile está en `deployment/Dockerfile`.
- Como la aplicación vive en `src/` y las dependencias en la raíz, el contexto de construcción de Docker debe ser la raíz del repositorio (`.`). El workflow debe apuntar al Dockerfile con la ruta `deployment/Dockerfile`.
- La variable `GROQ_API_KEY` debe proporcionarse al contenedor durante su ejecución, sin incorporarla a la imagen.

## Puesta en marcha en local

### 1. Clonar el repositorio

```bash
git clone https://github.com/victorlopez-ds/pj-asistente-accionista.git
cd pj-asistente-accionista
```

### 2. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Configurar la API Key de Groq

Crear una cuenta en:

https://console.groq.com/

Generar una API Key desde:

https://console.groq.com/keys

El archivo `.env.example` documenta la variable de entorno requerida.

Configurar la variable en la terminal antes de ejecutar la aplicación.

Linux/macOS:

```bash
export GROQ_API_KEY="your_groq_api_key_here"
```

Windows PowerShell:

```powershell
$env:GROQ_API_KEY = "your_groq_api_key_here"
```

La API Key es confidencial y nunca debe incorporarse al código fuente ni al repositorio de GitHub.

### 4. Ejecutar la aplicación

```bash
python -m uvicorn asistente_accionista.main:app --app-dir src --reload
```

La API estará disponible en:

http://127.0.0.1:8000

Documentación interactiva Swagger:

http://127.0.0.1:8000/docs

### 5. Consultar el endpoint

**POST /ask**

Ejemplo de solicitud:

```json
{
  "input": "¿Qué es el beneficio por acción?"
}
```

Ejemplo ilustrativo de respuesta:

```json
{
  "output": "El beneficio por acción es un indicador financiero que representa el beneficio atribuible a cada acción ordinaria de una empresa."
}
```

El contenido de la respuesta puede variar entre consultas.

### 6. Códigos de respuesta HTTP

| Código | Descripción |
|--------|-------------|
| 200 | Respuesta generada correctamente |
| 422 | Datos de entrada no válidos |
| 502 | Error de comunicación con el proveedor LLM |
| 503 | Servicio LLM no disponible |

## Funcionalidades previstas

- **Consulta de documentación en lenguaje natural:** permite realizar preguntas sobre la información disponible de una empresa mediante un asistente conversacional basado en RAG.
- **Respuestas con fuentes:** identifica los documentos y las fechas que respaldan la información proporcionada para que el usuario pueda consultar su origen.
- **Análisis de información a lo largo del tiempo:** facilita comparar distintos períodos e identificar cambios en los riesgos, las perspectivas y el discurso de la dirección de una empresa.
- **Contraste histórico con la cotización:** permite relacionar retrospectivamente determinadas afirmaciones o cambios de discurso con la evolución histórica de la cotización, con un propósito descriptivo y no predictivo.
- **Análisis cuantitativo experimental:** se plantea explorar modelos de aprendizaje automático para obtener estimaciones probabilísticas sobre series históricas de mercado, incluyendo incertidumbre y riesgo.
- **Preguntas de seguimiento:** funcionalidad avanzada prevista para mantener el contexto de la conversación y profundizar progresivamente en una empresa o cuestión.
- **Comparativa entre empresas:** funcionalidad avanzada planteada para facilitar el análisis comparativo de distintas compañías.
