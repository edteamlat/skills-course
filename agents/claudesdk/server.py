"""
Servidor web para el agente de fichas de películas.

Expone una interfaz de chat en el navegador que conversa con un agente del
Claude Agent SDK. El agente usa dos skills locales (`movies-finder` y
`movie-card-pdf`) para buscar la película y generar el PDF, que luego se
muestra al usuario en el navegador.
"""

import json
import logging
import re
from pathlib import Path

# FastAPI da el servidor HTTP; los Response* permiten devolver HTML, archivos
# y, lo más importante aquí, un stream SSE (Server-Sent Events) hacia el browser.
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel  # validación del body del POST /chat

# El SDK de Claude expone `query()` como un async generator: emite mensajes
# del agente conforme van llegando. Distinguimos los tipos de mensaje para
# decidir qué reenviar al frontend.
from claude_agent_sdk import (
    AssistantMessage,   # texto del agente (puede llegar varias veces)
    ClaudeAgentOptions, # configuración del agente (system prompt, tools, etc.)
    ResultMessage,      # mensaje final con costo / error
    TextBlock,          # bloque de texto dentro de un AssistantMessage
    query,
)

# Logging básico a stdout — útil para ver qué prompts entran en producción/dev.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# Rutas: todo lo estático (HTML del chat y los PDFs generados) vive en `static/`.
BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

# El system prompt es la "personalidad" e instrucciones del agente. Aquí le
# decimos:
#   - qué skill usar para buscar (movies-finder)
#   - qué skill usar para generar el PDF (movie-card-pdf)
#   - dónde y cómo nombrar el archivo (`static/<slug>.pdf`)
#   - que mencione la ruta en su respuesta para que el frontend la detecte
SYSTEM_PROMPT = """Eres un asistente especializado en películas que genera fichas en PDF.

Cuando el usuario te pida información sobre una película:
1. Usa la skill `movies-finder` para buscar la película y obtener sus detalles
   completos (incluye `--append credits` para traer el reparto).
2. Usa la skill `movie-card-pdf` para generar la ficha PDF a partir del JSON
   devuelto por `movies-finder`. La skill ya se encarga del formato; no edites
   su template ni inventes secciones.
3. Guarda SIEMPRE el PDF en la carpeta `static/` del proyecto (ruta relativa
   `static/<nombre>.pdf`), con el nombre de la película en minúsculas y guiones
   en lugar de espacios. Ejemplo: `static/la-vida-es-bella.pdf`.
4. En tu respuesta final menciona la ruta del PDF generado tal cual
   (`static/<nombre>.pdf`) para que la interfaz pueda mostrarlo.

Responde en español."""

# Opciones del agente:
# - setting_sources=["user", "project"]: hace que el SDK cargue la config de
#   ~/.claude (user) y de .claude/ del proyecto, donde viven las skills.
# - allowed_tools: el agente solo puede invocar Skill, Bash, Read y Write.
#   Suficiente para llamar a las skills y leer/escribir archivos auxiliares.
# - permission_mode="acceptEdits": auto-aprueba ediciones de archivos sin
#   prompts interactivos (estamos en un servidor, no hay TTY para preguntar).
OPTIONS = ClaudeAgentOptions(
    system_prompt=SYSTEM_PROMPT,
    setting_sources=["user", "project"],
    allowed_tools=["Skill", "Bash", "Read", "Write"],
    permission_mode="acceptEdits",
)

app = FastAPI(title="Agente de fichas de películas")
# Monta /static/* para servir el index.html y, de paso, cualquier asset estático.
# Los PDFs los servimos por una ruta dedicada (/pdf/...) para validar extensión.
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    """Body del POST /chat: solo el prompt del usuario."""
    prompt: str


@app.get("/", response_class=HTMLResponse)
async def index():
    """Sirve la UI del chat (HTML estático)."""
    return HTMLResponse((STATIC_DIR / "index.html").read_text(encoding="utf-8"))


@app.get("/pdf/{filename}")
async def serve_pdf(filename: str):
    """
    Sirve un PDF generado. Validamos que el archivo exista y tenga extensión
    .pdf para no convertir esta ruta en un descargador genérico.
    """
    pdf_path = STATIC_DIR / filename
    if not pdf_path.exists() or pdf_path.suffix != ".pdf":
        return HTMLResponse("PDF no encontrado", status_code=404)
    return FileResponse(str(pdf_path), media_type="application/pdf")


@app.post("/chat")
async def chat(request: ChatRequest):
    """
    Endpoint principal: recibe el prompt del usuario y devuelve un stream SSE
    con los mensajes del agente. El frontend (index.html) consume este stream
    y va pintando texto en el chat hasta recibir el evento `done`.
    """
    log.info("POST /chat prompt=%r", request.prompt[:80])

    async def event_stream():
        # Vamos a "escuchar" los mensajes del agente y, en paralelo, intentar
        # detectar la ruta del PDF generado para enviarla al final.
        pdf_file = None

        try:
            # query() es un async generator: cada `message` llega cuando el
            # agente lo emite (texto incremental, llamadas a tools, etc.).
            async for message in query(prompt=request.prompt, options=OPTIONS):
                # 1) Mensajes de texto del asistente → reenviar al browser.
                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock) and block.text:
                            # Heurística simple: si el agente mencionó
                            # `static/algo.pdf` en su texto, lo capturamos.
                            # El system prompt le pide hacerlo explícitamente.
                            match = re.search(r"static/([^\s\"']+\.pdf)", block.text)
                            if match:
                                pdf_file = match.group(1)
                            # Formato SSE: cada evento es `data: <json>\n\n`.
                            yield f"data: {json.dumps({'type': 'text', 'content': block.text})}\n\n"

                # 2) Mensaje final: el agente terminó. Enviamos costo, error
                #    (si hubo) y el nombre del PDF detectado para que el
                #    frontend lo cargue en el visor.
                elif isinstance(message, ResultMessage):
                    cost = (
                        f"${message.total_cost_usd:.4f}"
                        if message.total_cost_usd is not None
                        else None
                    )
                    yield f"data: {json.dumps({'type': 'done', 'cost': cost, 'error': message.result if message.is_error else None, 'pdf': pdf_file})}\n\n"

        except Exception as exc:
            # Cualquier excepción la convertimos en un evento `error` para que
            # el frontend pueda mostrarla en lugar de quedarse colgado.
            log.exception("error en event_stream")
            yield f"data: {json.dumps({'type': 'error', 'content': str(exc)})}\n\n"

    # media_type="text/event-stream" activa SSE en el browser (EventSource o
    # fetch + ReadableStream). El cliente recibe los eventos en tiempo real.
    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    # Modo desarrollo: uvicorn con reload para refrescar al guardar cambios.
    import uvicorn

    log.info("Iniciando servidor en http://localhost:8000")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
