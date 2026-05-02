"""
Servidor web para el agente de reportes de películas (versión OpenAI Agents SDK).
"""

import asyncio
import json
import logging
import os
import re
import shlex
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from agents import (
    Agent,
    Runner,
    ShellCommandOutput,
    ShellCommandRequest,
    ShellResult,
    ShellTool,
    ShellToolLocalEnvironment,
    ShellToolLocalSkill,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

# ── Executor local ──────────────────────────────────────────────────────────
#
# ShellTool con entorno local exige un executor que reciba ShellCommandRequest
# y ejecute comandos en el host. Usamos bash + subprocess.

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
            from agents import ShellCallOutcome

            outcome = ShellCallOutcome(type="exit", exit_code=proc.returncode)
            outputs.append(
                ShellCommandOutput(
                    stdout=stdout_b.decode("utf-8", errors="replace"),
                    stderr=stderr_b.decode("utf-8", errors="replace"),
                    outcome=outcome,
                    command=command,
                )
            )
        except asyncio.TimeoutError:
            proc.kill()
            await proc.wait()
            from agents import ShellCallOutcome

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

movies_skill: ShellToolLocalSkill = {
    "name": "movies-finder",
    "description": "Busca películas en la API de TMDB por título, género, año, puntuación o idioma.",
    "path": str(BASE_DIR / ".agents/skills/movies-finder"),
}

pdf_skill: ShellToolLocalSkill = {
    "name": "pdf",
    "description": "Crea y manipula reportes PDF usando reportlab.",
    "path": str(BASE_DIR / ".agents/skills/pdf"),
}

shell_environment: ShellToolLocalEnvironment = {
    "type": "local",
    "skills": [movies_skill, pdf_skill],
}

shell_tool = ShellTool(executor=local_shell_executor, environment=shell_environment)

# ── System prompt ───────────────────────────────────────────────────────────

SYSTEM_PROMPT = """Eres un asistente especializado en películas que crea reportes PDF.

Cuando el usuario te pida información sobre películas debes:
1. Usar el skill movies-finder para buscar y obtener los detalles completos
   de las películas solicitadas (incluyendo reparto, director, géneros, etc.)
2. Antes de invocar el skill pdf, lee el archivo `.agents/skills/movies-finder/assets/movie-response-template.md`
   (ruta relativa a la raíz del proyecto, el cwd actual) para obtener la estructura 
   del reporte final y el archivo `assets/pdf-theme.md` para el tema visual.
3. Usar el skill pdf para crear un reporte PDF bien formateado con toda
   la información recopilada. Al invocarlo, recuerda usar el template y el theme que están en 
   `.agents/skills/movies-finder/assets/movie-response-template.md` y `assets/pdf-theme.md` 
   en las instrucciones que le pases.
   Guarda siempre el PDF en la carpeta `static/` con un nombre descriptivo
   en minúsculas y sin espacios (ej: static/reporte_accion_2024.pdf)

Siempre termina generando el reporte PDF en la carpeta static/. Responde en español."""

# ── Agente ──────────────────────────────────────────────────────────────────

agent = Agent(
    name="movies-agent",
    instructions=SYSTEM_PROMPT,
    tools=[shell_tool],
    model="gpt-5.4",
)

# ── FastAPI ──────────────────────────────────────────────────────────────────

app = FastAPI(title="Agente de Reportes de Películas")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    prompt: str


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = BASE_DIR / "static" / "index.html"
    log.info("GET / → sirviendo index.html")
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/pdf/{filename}")
async def serve_pdf(filename: str):
    pdf_path = STATIC_DIR / filename
    log.info("GET /pdf/%s → existe=%s", filename, pdf_path.exists())
    if not pdf_path.exists() or pdf_path.suffix != ".pdf":
        return HTMLResponse("PDF no encontrado", status_code=404)
    return FileResponse(str(pdf_path), media_type="application/pdf")


PDF_RE = re.compile(r"static/([^\s\"']+\.pdf)")


@app.post("/chat")
async def chat(request: ChatRequest):
    log.info("POST /chat prompt=%r", request.prompt[:80])

    async def event_stream():
        pdf_file: str | None = None

        try:
            result = Runner.run_streamed(agent, input=request.prompt)

            async for event in result.stream_events():
                # Deltas de texto del modelo (streaming token a token)
                if event.type == "raw_response_event":
                    data = event.data
                    delta_type = getattr(data, "type", None)
                    if delta_type == "response.output_text.delta":
                        text = getattr(data, "delta", "") or ""
                        if text:
                            m = PDF_RE.search(text)
                            if m:
                                pdf_file = m.group(1)
                            payload = json.dumps({"type": "text", "content": text})
                            yield f"data: {payload}\n\n"

                # Items completos (útil para capturar texto final completo
                # por si algún delta se perdió)
                elif event.type == "run_item_stream_event":
                    if event.name == "message_output_created":
                        item = event.item
                        text = getattr(item, "raw_item", None)
                        # item.raw_item es el output del modelo; intentamos
                        # extraer texto para detectar PDFs referenciados.
                        try:
                            from agents import ItemHelpers

                            full = ItemHelpers.text_message_output(item)
                            if full:
                                m = PDF_RE.search(full)
                                if m:
                                    pdf_file = m.group(1)
                        except Exception:
                            pass

            # Fallback: si no detectamos el PDF en el texto, usamos el más reciente
            if pdf_file is None:
                pdfs = sorted(STATIC_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime)
                if pdfs:
                    pdf_file = pdfs[-1].name
                    log.info("PDF detectado por mtime: %s", pdf_file)
                else:
                    log.warning("no se encontró ningún PDF en static/")

            payload = json.dumps({"type": "done", "pdf": pdf_file})
            yield f"data: {payload}\n\n"

        except Exception as exc:
            log.exception("excepción en event_stream: %s", exc)
            payload = json.dumps({"type": "error", "content": str(exc)})
            yield f"data: {payload}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    log.info("Iniciando servidor en http://localhost:8000")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
