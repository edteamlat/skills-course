# Agente de fichas de películas (OpenAI Agents SDK)

Agente de IA que busca información de películas y genera fichas en PDF, usando el **OpenAI Agents SDK** con skills locales. Interfaz de chat web.

Versión equivalente a `claudesdk/` pero orquestada con `openai-agents` en lugar de `claude-agent-sdk`.

## Skills usadas

Ambas viven en `.agents/skills/`:

- **movies-finder** — busca y consulta películas en TMDB
- **movie-card-pdf** — genera la ficha PDF a partir del JSON de TMDB

A diferencia de la versión Claude (donde las skills se descubren automáticamente desde `.claude/skills/`), aquí se registran explícitamente como `ShellToolLocalSkill` en `server.py`.

## Requisitos

- Python 3.10+
- `bash` y `curl` disponibles (los usa `movies-finder`)
- Chrome/Chromium (lo usa `movie-card-pdf` para renderizar el PDF)
- API key de OpenAI
- Token de acceso a la API de TMDB

## Instalación

```bash
python3 -m venv ./venv
source ./venv/bin/activate
pip3 install -r requirements.txt
cp .env.example .env
# editar .env y poner OPENAI_API_KEY y TMDB_ACCESS_TOKEN
```

- Token de TMDB: https://www.themoviedb.org/settings/api (campo "API Read Access Token").
- API key de OpenAI: https://platform.openai.com/api-keys

## Uso

```bash
python3 server.py
```

Abre http://localhost:8000. Escribe la película en el chat; el PDF generado aparecerá en el panel derecho.

## Modelo

El agente usa `gpt-5.4`. El `ShellTool` con entorno local **no es compatible** con la familia `gpt-4o` — si cambias el modelo, usa uno que soporte la herramienta `shell` hospedada (`gpt-4.1`, `gpt-5`, `gpt-5.4`).
