"""
Servidor web para el agente de fichas de películas (versión OpenAI Agents SDK).

Expone una interfaz de chat en el navegador que conversa con un agente del
OpenAI Agents SDK. El agente usa dos skills locales (`movies-finder` y
`movie-card-pdf`) para buscar la película y generar el PDF, que luego se
muestra al usuario en el navegador.
"""

import asyncio
import json
import logging
import re
from pathlib import Path

from dotenv import load_dotenv

# FastAPI da el servidor HTTP; los Response* permiten devolver HTML, archivos
# y, lo más importante aquí, un stream SSE (Server-Sent Events) hacia el browser.
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel  # validación del body del POST /chat

# OpenAI Agents SDK: ShellTool habilita ejecución de comandos. A diferencia del
# Claude Agent SDK (que descubre skills automáticamente desde `.claude/`), aquí
# las skills se registran explícitamente como ShellToolLocalSkill apuntando a
# carpetas con un SKILL.md. El executor local corre los comandos en el host.
from agents import (
    Agent,
    Runner,
    ShellCallOutcome,
    ShellCommandOutput,
    ShellCommandRequest,
    ShellResult,
    ShellTool,
    ShellToolLocalEnvironment,
    ShellToolLocalSkill,
)

load_dotenv()

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


# ── Executor local del ShellTool ────────────────────────────────────────────
#
# ShellTool con entorno local exige un executor que reciba ShellCommandRequest
# y ejecute los comandos en el host. Usamos asyncio.subprocess + bash.
DEFAULT_TIMEOUT_MS = 120_000


async def local_shell_executor(request: ShellCommandRequest) -> ShellResult:
    action = request.data.action
    timeout_s = (action.timeout_ms or DEFAULT_TIMEOUT_MS) / 1000
    outputs: list[ShellCommandOutput] = []

    for command in action.commands:
        log.info("shell exec: %s", command[:160])
        proc = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=str(BASE_DIR),
            executable="/bin/bash",
        )
        try:
            stdout_b, stderr_b = await asyncio.wait_for(
                proc.communicate(), timeout=timeout_s
            )
            outputs.append(
                ShellCommandOutput(
                    stdout=stdout_b.decode("utf-8", errors="replace"),
                    stderr=stderr_b.decode("utf-8", errors="replace"),
                    outcome=ShellCallOutcome(type="exit", exit_code=proc.returncode),
                    command=command,
                )
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            outputs.append(
                ShellCommandOutput(
                    stdout="",
                    stderr=f"command timed out after {timeout_s}s",
                    outcome=ShellCallOutcome(type="timeout"),
                    command=command,
                )
            )

    return ShellResult(output=outputs, max_output_length=action.max_output_length)


# ── Skills locales ──────────────────────────────────────────────────────────
#
# Cada skill es una carpeta con un SKILL.md. El SDK lee el SKILL.md cuando el
# agente decide invocarla y le entrega esas instrucciones al modelo.
movies_skill: ShellToolLocalSkill = {
    "name": "movies-finder",
    "description": "Busca películas en la API de TMDB por título, género, año, puntuación o idioma.",
    "path": str(BASE_DIR / ".agents/skills/movies-finder"),
}

movie_card_skill: ShellToolLocalSkill = {
    "name": "movie-card-pdf",
    "description": "Genera una ficha PDF de una película a partir del JSON de TMDB.",
    "path": str(BASE_DIR / ".agents/skills/movie-card-pdf"),
}

shell_environment: ShellToolLocalEnvironment = {
    "type": "local",
    "skills": [movies_skill, movie_card_skill],
}

shell_tool = ShellTool(executor=local_shell_executor, environment=shell_environment)


# ── System prompt ───────────────────────────────────────────────────────────
#
# El system prompt define la "personalidad" e instrucciones del agente. Aquí le
# decimos:
#   - qué skill usar para buscar (movies-finder)
#   - qué skill usar para generar el PDF (movie-card-pdf)
#   - dónde y cómo nombrar el archivo (`static/<slug>.pdf`)
#   - que mencione la ruta en su respuesta para que el frontend la detecte
SYSTEM_PROMPT = """Eres un asistente especializado en películas que genera fichas en PDF.

REGLA INVIOLABLE: tu única forma de entregar resultados al usuario es generando
un PDF con la skill `movie-card-pdf`. NO resumas la película en texto, NO listes
los datos en el chat, NO entregues la ficha en formato Markdown. El usuario solo
quiere el PDF.

Flujo OBLIGATORIO para cada solicitud:
1. Usa la skill `movies-finder` para obtener el JSON de la película.
2. Usa la skill `movie-card-pdf` para generar el PDF a partir de ese JSON.
   No saltes este paso. No respondas sin haberlo ejecutado.
3. Asegúrate de que el PDF final exista en `static/<slug>.pdf` **respecto a la
   raíz del proyecto** (la carpeta donde corre el servidor, NO una subcarpeta).
   Si la skill generó el PDF en otra ubicación (por ejemplo dentro de la
   carpeta de la skill o en `/tmp/`), cópialo o muévelo a `static/<slug>.pdf`
   desde la raíz del proyecto antes de responder. Verifícalo con
   `ls static/<slug>.pdf` desde la raíz.
   `<slug>` es el nombre de la película en minúsculas, sin acentos y con
   guiones en lugar de espacios. Ejemplo: "La vida es bella" → `static/la-vida-es-bella.pdf`.
4. Responde EXACTAMENTE con: "Listo, generé la ficha en `static/<slug>.pdf`."
   Nada más. No agregues sinopsis, datos, ni listas — todo eso ya está en el PDF.

Responde en español."""


# ── Agente ──────────────────────────────────────────────────────────────────
#
# ShellTool con entorno local NO es compatible con la familia gpt-4o; usamos
# gpt-5.4 (también funcionan gpt-4.1 y gpt-5).
agent = Agent(
    name="movies-agent",
    instructions=SYSTEM_PROMPT,
    tools=[shell_tool],
    model="gpt-5.4",
)


# ── FastAPI ──────────────────────────────────────────────────────────────────

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


PDF_RE = re.compile(r"static/([^\s\"']+\.pdf)")


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
        pdf_file: str | None = None

        try:
            # Runner.run_streamed devuelve un objeto con `stream_events()`,
            # un async generator de eventos del agente (deltas de texto,
            # llamadas a tools, etc.).
            result = Runner.run_streamed(agent, input=request.prompt)

            async for event in result.stream_events():
                # Deltas de texto del modelo (streaming token a token).
                # raw_response_event con type=response.output_text.delta es el
                # equivalente a recibir trozos del texto del asistente.
                if event.type == "raw_response_event":
                    data = event.data
                    if getattr(data, "type", None) == "response.output_text.delta":
                        text = getattr(data, "delta", "") or ""
                        if text:
                            # Heurística simple: si el agente mencionó
                            # `static/algo.pdf` en su texto, lo capturamos.
                            # El system prompt le pide hacerlo explícitamente.
                            match = PDF_RE.search(text)
                            if match:
                                pdf_file = match.group(1)
                            # Formato SSE: cada evento es `data: <json>\n\n`.
                            yield f"data: {json.dumps({'type': 'text', 'content': text})}\n\n"

                # Item completo del agente. Cuando hay turnos con tool calls,
                # el texto final del último turno a veces no llega partido en
                # deltas: aquí lo agarramos completo para detectar el PDF.
                # NO reenviamos texto al frontend (los deltas ya lo hicieron),
                # solo extraemos la ruta del PDF si aparece.
                elif event.type == "run_item_stream_event" and event.name == "message_output_created":
                    try:
                        from agents import ItemHelpers

                        full = ItemHelpers.text_message_output(event.item)
                        if full:
                            match = PDF_RE.search(full)
                            if match:
                                pdf_file = match.group(1)
                    except Exception:
                        log.debug("no pude extraer texto de message_output_created", exc_info=True)

            # Mensaje final: el agente terminó. Enviamos el nombre del PDF
            # detectado para que el frontend lo cargue en el visor.
            yield f"data: {json.dumps({'type': 'done', 'pdf': pdf_file})}\n\n"

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
