# Agente de fichas de películas

Agente de IA que busca información de películas y genera fichas en PDF, usando el Claude Agent SDK con skills locales. Interfaz de chat web.

## Skills usadas

Ambas viven en `.claude/skills/`:

- **movies-finder** — busca y consulta películas en TMDB
- **movie-card-pdf** — genera la ficha PDF a partir del JSON de TMDB

## Requisitos

- Python 3.10+
- Claude Code CLI instalado y autenticado
- Token de acceso a la API de TMDB
- Chrome/Chromium (lo usa `movie-card-pdf` para renderizar el PDF)

## Instalación

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install claude-agent-sdk fastapi "uvicorn[standard]"
cp .env.example .env
# editar .env y poner el TMDB_ACCESS_TOKEN
```

Token en: https://www.themoviedb.org/settings/api (campo "API Read Access Token").

## Uso

```bash
python3 server.py
```

Abre http://localhost:8000. Escribe la película en el chat; el PDF generado aparecerá en el panel derecho.
