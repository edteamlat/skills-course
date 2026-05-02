# Agente de reportes de películas (OpenAI Agents SDK)

Agente de IA que busca información de películas y genera reportes en PDF, usando el **OpenAI Agents SDK** con skills locales. Disponible como CLI y como aplicación web con interfaz de chat.

Esta es la versión equivalente al proyecto `claudesdk/` pero orquestada con `openai-agents` en lugar de `claude-agent-sdk`.

## Requisitos

- Python 3.10+
- `bash` y `curl` disponibles en el sistema (los usa el skill `movies-finder` internamente)
- Una API key de OpenAI
- Un token de acceso a la API de TMDB

## Instalación

### 1. Crear y activar el entorno virtual

```bash
python3 -m venv ./venv
source ./venv/bin/activate
```

### 2. Instalar las dependencias

```bash
pip3 install -r requirements.txt
```

Equivale a:

```bash
pip3 install openai-agents fastapi "uvicorn[standard]" python-dotenv reportlab
```

### 3. Configurar las variables de entorno

Copia el archivo de ejemplo y agrega tus credenciales:

```bash
cp .env.example .env
```

Edita `.env` y reemplaza los valores:

```
TMDB_ACCESS_TOKEN=tu_token_de_tmdb
OPENAI_API_KEY=sk-...
```

- Token de TMDB: https://www.themoviedb.org/settings/api (campo "API Read Access Token").
- API key de OpenAI: https://platform.openai.com/api-keys

### 4. Verificar permisos de ejecución de los scripts de skills

Los scripts de los skills deben ser ejecutables:

```bash
chmod +x .agents/skills/movies-finder/scripts/*.sh
chmod +x .agents/skills/pdf/scripts/*.py
```

## Uso

### Modo web (interfaz de chat)

```bash
python3 -m uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

O directamente:

```bash
python3 server.py
```

Abre http://localhost:8000 en tu navegador. Escribe tu solicitud en el chat y el PDF generado aparecerá automáticamente en el panel derecho.

### Modo CLI — argumento

```bash
python3 agent.py "Crea un reporte PDF de las 5 películas de acción mejor puntuadas de 2024"
```

### Modo CLI — interactivo

```bash
python3 agent.py
```

El agente te pedirá que escribas tu solicitud.

## Ejemplos de solicitudes

```bash
python3 agent.py "Crea un reporte PDF con las 3 películas más populares del momento"

python3 agent.py "Genera un reporte de las mejores películas de ciencia ficción de Christopher Nolan"

python3 agent.py "Busca la película Interstellar y crea un reporte PDF con sus detalles"

python3 agent.py "Reporte PDF de comedias en español del 2023 con puntuación mayor a 7"
```

## Cómo funciona

El agente usa el **OpenAI Agents SDK** (`openai-agents`) y se le pasan explícitamente los skills locales mediante `ShellToolLocalSkill`, cada uno apuntando a un directorio que contiene un `SKILL.md`:

- **movies-finder** — consulta la API de TMDB para buscar películas, obtener detalles, reparto, director y más.
- **pdf** — crea el reporte PDF con la información recopilada.

A diferencia de la versión Claude (donde los skills se descubren automáticamente desde `.claude/skills/`), aquí los skills se referencian explícitamente en el código (`server.py`), y el `ShellTool` se ejecuta con un **executor local propio** basado en `asyncio.subprocess` + bash que corre los comandos en el host.

El agente lee cada `SKILL.md` cuando lo necesita y ejecuta sus scripts según las instrucciones que contiene.

En el modo web, el servidor expone un endpoint `/chat` con streaming (SSE) que transmite la respuesta del agente al navegador en tiempo real. El PDF generado se sirve desde la carpeta `static/` y se muestra en un visor integrado.

## Modelo

El agente está configurado con `gpt-5.4`. El `ShellTool` con entorno local **no es compatible** con modelos de la familia `gpt-4o` — si cambias el modelo, asegúrate de usar uno que soporte la herramienta `shell` hospedada (`gpt-4.1`, `gpt-5`, `gpt-5.4`).

## Estructura del proyecto

```
openaisdk/
├── agent.py                        # Punto de entrada CLI del agente
├── server.py                       # Servidor web (FastAPI + SSE + executor local)
├── requirements.txt                # Dependencias de Python
├── assets/
│   └── pdf-theme.md                # Tema visual del reporte PDF
├── static/
│   └── index.html                  # Interfaz de chat web
├── .env                            # OPENAI_API_KEY + TMDB_ACCESS_TOKEN (no subir a git)
├── .env.example                    # Plantilla de configuración
└── .agents/
    └── skills/
        ├── movies-finder/          # Skill para consultar películas
        │   ├── SKILL.md
        │   └── scripts/
        │       └── movies.sh
        └── pdf/                    # Skill para crear PDFs
            ├── SKILL.md
            └── scripts/
```

## Solución de problemas

- **`The api_key client option must be set...`** — falta `OPENAI_API_KEY` en `.env`, o el servidor se arrancó antes de crear el archivo. Reinicia el servidor.
- **`Tool 'shell' is not supported with gpt-4o`** — estás usando un modelo incompatible. Usa `gpt-5.4` (o `gpt-4.1` / `gpt-5`).
- **`Permission denied` al ejecutar `movies.sh`** — aplica `chmod +x` a los scripts (paso 4 de la instalación).
- **No se encuentra el PDF** — revisa los logs del servidor para ver errores del skill `pdf`. El archivo debe quedar en `static/` con extensión `.pdf`.
