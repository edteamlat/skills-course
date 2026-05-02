"""
Punto de entrada CLI del agente de reportes de películas (versión OpenAI Agents SDK).
"""

import asyncio
import sys
from pathlib import Path

from dotenv import load_dotenv

from agents import Agent, Runner
from server import shell_tool, SYSTEM_PROMPT

load_dotenv()

BASE_DIR = Path(__file__).parent

agent = Agent(
    name="movies-agent",
    instructions=SYSTEM_PROMPT,
    tools=[shell_tool],
    model="gpt-5.4",
)


async def run(prompt: str) -> None:
    print(f"\nSolicitud: {prompt}\n")
    print("─" * 60)
    result = await Runner.run(agent, input=prompt)
    print(result.final_output)
    print("─" * 60)


def main() -> None:
    if len(sys.argv) > 1:
        prompt = " ".join(sys.argv[1:])
    else:
        print("Agente de reportes de películas (OpenAI)\n")
        prompt = input("Tu solicitud: ").strip()
        if not prompt:
            prompt = "Crea un reporte PDF con las 3 películas más populares del momento"
    asyncio.run(run(prompt))


if __name__ == "__main__":
    main()
