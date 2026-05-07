#!/usr/bin/env python3
"""
Renderiza una ficha de película a PDF usando Chrome/Chromium headless.

Dependencias: solo Python 3.10+ stdlib + un navegador Chromium-based
              (Google Chrome, Chromium, Brave o Microsoft Edge).

Uso:
    python render.py --data ruta/al/json --out ruta/al/pdf
    python render.py --data ... --out ... --chrome /ruta/al/binario  # opcional
"""
from __future__ import annotations

import argparse
import html
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from string import Template

MESES_ES = {
    1: "enero", 2: "febrero", 3: "marzo", 4: "abril",
    5: "mayo", 6: "junio", 7: "julio", 8: "agosto",
    9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre",
}

MAX_PROTAGONISTAS = 5

CHROME_PATHS = {
    "darwin": [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    ],
    "linux": [
        "google-chrome", "google-chrome-stable", "chromium",
        "chromium-browser", "microsoft-edge", "brave-browser",
    ],
    "win32": [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    ],
}


def encontrar_chrome(override: str | None = None) -> str:
    if override:
        if not Path(override).exists():
            raise FileNotFoundError(f"--chrome no existe: {override}")
        return override

    if (env := os.environ.get("CHROME_BIN")) and Path(env).exists():
        return env

    plataforma = "darwin" if sys.platform == "darwin" else (
        "win32" if sys.platform == "win32" else "linux"
    )
    for c in CHROME_PATHS.get(plataforma, []):
        if "/" in c or "\\" in c:
            if Path(c).exists():
                return c
        elif (ruta := shutil.which(c)):
            return ruta

    raise RuntimeError(
        "No se encontró Chrome/Chromium. Instala Google Chrome, Chromium, "
        "Brave o Edge, o pasa la ruta con --chrome / CHROME_BIN."
    )


def fecha_es(release_date: str) -> tuple[str, str]:
    if not release_date:
        return "", ""
    try:
        y, m, d = release_date.split("-")
        return y, f"{int(d)} de {MESES_ES[int(m)]} de {y}"
    except (ValueError, KeyError) as e:
        raise ValueError(f"release_date mal formateada: {release_date!r}") from e


def duracion_humana(runtime_min) -> str:
    if not isinstance(runtime_min, (int, float)) or runtime_min <= 0:
        return ""
    h, m = divmod(int(runtime_min), 60)
    if h == 0:
        return f"{m}min"
    return f"{h}h" if m == 0 else f"{h}h {m}min"


def transformar(raw: dict) -> dict:
    anio, fecha = fecha_es(raw.get("release_date", ""))
    cast = sorted(raw.get("credits", {}).get("cast", []) or [],
                  key=lambda c: c.get("order", 999))
    n = min(len(cast), MAX_PROTAGONISTAS)

    return {
        "titulo": raw.get("title", ""),
        "anio": anio,
        "puntuacion": round(float(raw.get("vote_average", 0.0)), 1),
        "fecha_estreno": fecha,
        "duracion": duracion_humana(raw.get("runtime")),
        "generos": [g["name"] for g in raw.get("genres", []) if "name" in g],
        "protagonistas": [c["name"] for c in cast[:n]],
        "otros_mas": max(0, len(cast) - n),
        "sinopsis": (raw.get("overview") or "").strip() or "Sin sinopsis disponible.",
    }


def construir_html(datos: dict, template_path: Path) -> str:
    """Sustituye los placeholders del template HTML.

    Los condicionales se manejan toggleando style="display:none" en los
    elementos correspondientes, así todo el HTML/SVG vive en el template.
    """
    safe = html.escape
    hide = 'style="display:none"'

    return Template(template_path.read_text(encoding="utf-8")).substitute(
        titulo=safe(datos["titulo"]),
        anio=safe(datos["anio"]),
        puntuacion=datos["puntuacion"],
        fecha_estreno=safe(datos["fecha_estreno"]),
        duracion=safe(datos["duracion"]),
        duracion_display="" if datos["duracion"] else hide,
        generos=safe(", ".join(datos["generos"])),
        protagonistas=safe(", ".join(datos["protagonistas"])),
        otros_mas=datos["otros_mas"],
        otros_mas_display="" if datos["otros_mas"] > 0 else hide,
        sinopsis=safe(datos["sinopsis"]),
    )


def html_a_pdf(html_str: str, out_path: Path, chrome_bin: str) -> None:
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(tmp) / "page.html"
        page.write_text(html_str, encoding="utf-8")
        cmd = [
            chrome_bin, "--headless", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer", "--hide-scrollbars",
            f"--print-to-pdf={out_path}", page.as_uri(),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        if r.returncode != 0 or not out_path.exists():
            raise RuntimeError(f"Chrome falló ({r.returncode}):\n{r.stderr}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--chrome", help="Ruta al binario de Chrome (opcional)")
    args = ap.parse_args()

    base = Path(__file__).resolve().parent.parent
    raw = json.loads(Path(args.data).read_text(encoding="utf-8"))
    html_str = construir_html(transformar(raw), base / "templates" / "card.html")
    html_a_pdf(html_str, Path(args.out).resolve(), encontrar_chrome(args.chrome))

    print(f"PDF generado: {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
