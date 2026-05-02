# Agente de reportes de películas

Agente de IA que busca información de películas y genera reportes en PDF, usando el Claude Agent SDK con skills locales. Disponible como CLI y como aplicación web con interfaz de chat.

## Requisitos

- Python 3.10+
- Claude Code CLI instalado y autenticado
- Token de acceso a la API de TMDB

## Instalación

### 1. Crear y activar el entorno virtual

```bash
python3 -m venv ./venv
source ./venv/bin/activate
```

### 2. Instalar las dependencias

```bash
pip3 install claude-agent-sdk fastapi "uvicorn[standard]"
```

### 3. Configurar el token de TMDB

Copia el archivo de ejemplo y agrega tu token:

```bash
cp .env.example .env
```

Edita `.env` y reemplaza el valor:

```
TMDB_ACCESS_TOKEN=tu_token_aqui
```

Obtén tu token en: https://www.themoviedb.org/settings/api (campo "API Read Access Token").

## Uso

### Modo web (interfaz de chat)

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

El agente usa el **Claude Agent SDK** y descubre automáticamente los skills disponibles en `.claude/skills/`:

- **movies-finder** — consulta la API de TMDB para buscar películas, obtener detalles, reparto, director y más.
- **pdf** — crea el reporte PDF con la información recopilada.

El agente no conoce los scripts internos de cada skill. Claude lee el `SKILL.md` de cada skill cuando lo necesita y ejecuta sus scripts según las instrucciones que contiene.

En el modo web, el servidor expone un endpoint `/chat` con streaming (SSE) que transmite la respuesta del agente al navegador en tiempo real. El PDF generado se sirve desde la carpeta `static/` y se muestra en un visor integrado.

## Estructura del proyecto

```
claudesdk/
├── agent.py                        # Punto de entrada CLI del agente
├── server.py                       # Servidor web (FastAPI + SSE)
├── static/
│   └── index.html                  # Interfaz de chat web
├── .env                            # Token de TMDB (no subir a git)
├── .env.example                    # Plantilla de configuración
└── .claude/
    └── skills/
        ├── movies-finder/          # Skill para consultar películas
        │   ├── SKILL.md
        │   └── scripts/
        │       └── movies.sh
        └── pdf/                    # Skill para crear PDFs
            ├── SKILL.md
            └── scripts/
```
