"""
Agente de IA para crear reportes PDF de películas.

Usa el Claude Agent SDK con los skills disponibles en .claude/skills/:
  - movies-finder: busca y consulta información de películas (TMDB)
  - pdf: crea reportes PDF con la información recopilada

El agente descubre y usa los skills automáticamente. No conoce
los scripts internos de cada skill.
"""

import asyncio
import sys

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    query,
)

# ──────────────────────────────────────────────
# Configuración del agente
# ──────────────────────────────────────────────

SYSTEM_PROMPT = """Eres un asistente especializado en películas que crea reportes PDF.

Cuando el usuario te pida información sobre películas debes:
1. Usar el skill movies-finder para buscar y obtener los detalles completos
   de las películas solicitadas (incluyendo reparto, director, géneros, etc.)
2. Antes de invocar el skill pdf, lee el archivo `.claude/skills/movie-finder/assets/movie-response-template.md`
   (ruta relativa a la raíz del proyecto, el cwd actual) para obtener la estructura 
   del reporte final y el archivo `assets/pdf-theme.md` para el tema visual.
3. Usar el skill pdf para crear un reporte PDF bien formateado con toda
   la información recopilada. Al invocarlo, recuerda usar el theme y el template que están
   en `.claude/skills/movie-finder/assets/movie-response-template.md` y `assets/pdf-theme.md` 
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


# ──────────────────────────────────────────────
# Ejecución del agente
# ──────────────────────────────────────────────

async def run(prompt: str) -> None:
    print(f"\nSolicitud: {prompt}\n")
    print("─" * 60)

    async for message in query(prompt=prompt, options=OPTIONS):
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if isinstance(block, TextBlock) and block.text:
                    print(block.text)
        elif isinstance(message, ResultMessage):
            print("─" * 60)
            if message.total_cost_usd is not None:
                print(f"Costo: ${message.total_cost_usd:.4f}")
            if message.is_error:
                print(f"Error: {message.result}")


def main() -> None:
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("Agente de reportes de películas")
        print('Ejemplo: "Crea un reporte PDF de las 3 películas más populares de ciencia ficción"\n')
        prompt = input("Tu solicitud: ").strip()
        if not prompt:
            prompt = "Crea un reporte PDF con las 3 películas más populares del momento"

    asyncio.run(run(prompt))


if __name__ == "__main__":
    main()
