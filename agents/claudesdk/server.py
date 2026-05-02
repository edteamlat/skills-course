"""
Servidor web para el agente de reportes de películas.

Expone una interfaz de chat en el navegador con visualización del PDF generado.
"""

import json
import logging
import re
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent
STATIC_DIR = BASE_DIR / "static"
STATIC_DIR.mkdir(exist_ok=True)

SYSTEM_PROMPT = """Eres un asistente especializado en películas que crea reportes PDF.

Cuando el usuario te pida información sobre películas debes:
1. Usar el skill movies-finder para buscar y obtener los detalles completos
   de las películas solicitadas (incluyendo reparto, director, géneros, etc.)
2. Antes de invocar el skill pdf, lee el archivo `.claude/skills/movies-finder/assets/movie-response-template.md`
   (ruta relativa a la raíz del proyecto, el cwd actual) para obtener la estructura 
   del reporte final y el archivo `assets/pdf-theme.md` para el tema visual.
3. Usar el skill pdf para crear un reporte PDF bien formateado con toda
   la información recopilada. Al invocarlo, incluye íntegramente el contenido
   de `.claude/skills/movies-finder/assets/movie-response-template.md` y `assets/pdf-theme.md` 
   en las instrucciones que le pases.
   Guarda siempre el PDF en la carpeta `static/` con un nombre descriptivo
   en minúsculas y sin espacios (ej: static/reporte_accion_2024.pdf)

Siempre termina generando el reporte PDF en la carpeta static/. Responde en español."""

OPTIONS = ClaudeAgentOptions(
    system_prompt=SYSTEM_PROMPT,
    setting_sources=["user", "project"],
    allowed_tools=["Skill", "Bash", "Read", "Write"],
    permission_mode="acceptEdits",
)

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
    log.info("GET /pdf/%s → %s (existe=%s)", filename, pdf_path, pdf_path.exists())
    if not pdf_path.exists() or pdf_path.suffix != ".pdf":
        return HTMLResponse("PDF no encontrado", status_code=404)
    return FileResponse(str(pdf_path), media_type="application/pdf")


@app.post("/chat")
async def chat(request: ChatRequest):
    log.info("POST /chat prompt=%r", request.prompt[:80])

    async def event_stream():
        pdf_file = None
        msg_count = 0

        try:
            async for message in query(prompt=request.prompt, options=OPTIONS):
                msg_count += 1
                log.debug("mensaje #%d tipo=%s", msg_count, type(message).__name__)

                if isinstance(message, AssistantMessage):
                    for block in message.content:
                        if isinstance(block, TextBlock) and block.text:
                            log.debug("TextBlock (%d chars)", len(block.text))
                            match = re.search(r"static/([^\s\"']+\.pdf)", block.text)
                            if match:
                                pdf_file = match.group(1)
                                log.info("PDF detectado en texto: %s", pdf_file)

                            data = json.dumps({"type": "text", "content": block.text})
                            yield f"data: {data}\n\n"

                elif isinstance(message, ResultMessage):
                    log.info(
                        "ResultMessage is_error=%s cost=%s",
                        message.is_error,
                        message.total_cost_usd,
                    )
                    if message.is_error:
                        log.error("error del agente: %s", message.result)

                    if pdf_file is None:
                        pdfs = sorted(
                            STATIC_DIR.glob("*.pdf"), key=lambda p: p.stat().st_mtime
                        )
                        if pdfs:
                            pdf_file = pdfs[-1].name
                            log.info("PDF detectado por mtime: %s", pdf_file)
                        else:
                            log.warning("no se encontró ningún PDF en static/")

                    cost = (
                        f"${message.total_cost_usd:.4f}"
                        if message.total_cost_usd is not None
                        else None
                    )
                    data = json.dumps(
                        {
                            "type": "done",
                            "cost": cost,
                            "error": message.result if message.is_error else None,
                            "pdf": pdf_file,
                        }
                    )
                    yield f"data: {data}\n\n"

        except Exception as exc:
            log.exception("excepción en event_stream: %s", exc)
            data = json.dumps({"type": "error", "content": str(exc)})
            yield f"data: {data}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn

    log.info("Iniciando servidor en http://localhost:8000")
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
