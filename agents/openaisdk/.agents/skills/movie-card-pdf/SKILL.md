---
name: movie-card-pdf
description: Úsala SIEMPRE que el usuario quiera generar un PDF tipo ficha de película a partir de los datos de una película. Incluso si el usuario solo pega un JSON con datos de película, dice "arma la ficha en PDF", "exporta esto a PDF" o pide convertir información de una película a PDF, úsala. 
---

# Generación de fichas de película en PDF

## Cuándo usar esta skill

Cuando se te entregue un JSON de película y se pida generar un PDF, una "ficha", o exportar la información a PDF.

Si los datos vienen de otra skill que consulta TMDB, esa skill se encarga de traer el JSON; esta skill solo se encarga de renderizarlo a PDF.

## Esquema esperado del input

JSON con la forma de la respuesta de TMDB. Campos relevantes:

- `title` (string) — obligatorio
- `release_date` (AAAA-MM-DD) — obligatorio
- `vote_average` (float) — obligatorio
- `runtime` (int, minutos) — opcional, se omite del PDF si falta
- `genres` (lista de objetos `{name: ...}`)
- `credits.cast` (lista de objetos `{name: ..., order: ...}`)
- `overview` (string) — si está vacío se usa "Sin sinopsis disponible."

Cualquier otro campo se ignora.

## Flujo de uso

1. Guarda el JSON de entrada en disco (por ejemplo `/tmp/pelicula.json`).
2. Ejecuta el script:

   ```bash
   python3 scripts/render.py --data /tmp/pelicula.json --out static/{{pelicula}}.pdf
   ```
Nota: {{pelicula}} es el nombre de la película que se está generando, sin espacios, reemplaza los espacios con guiones.

3. Entrega el PDF resultante al usuario.

`render.py` aplica internamente todas las transformaciones (fecha en
español, redondeo de puntuación a 1 decimal, conversión de runtime a
"Xh Ymin", ordenamiento de cast por `order`, recorte a los primeros 5
protagonistas, etc.). **No formatees los datos antes de pasarlos**:
entrega el JSON tal como lo devuelve la API.

## Reglas estrictas (no negociables)

- **No edites** `templates/card.html` para una generación puntual. 
- **No agregues secciones** que no estén en el template (no inventes "Director", "Premios", "Trailer", etc.).
- **No completes datos faltantes** con valores inventados. El script ya maneja las omisiones automáticamente.
- **Si añades nuevas variables al template**, recuerda que `string.Template` no acepta caracteres no-ASCII (ñ, acentos) en los nombres de las
  variables. Usa `anio` en vez de `año`, `duracion` en vez de `duración`.

## Dependencias

**Python:** Python 3.10+

**Navegador:** Chrome/Chromium en modo headless. El script detecta
automáticamente cualquiera de Google Chrome, Chromium, Brave o Microsoft
Edge.

Si no lo detecta o quieres forzar uno específico:

```bash
export CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
# o:
python3 scripts/render.py --data ... --out ... --chrome "/ruta/a/chrome"
```

Si no tienes ningún navegador instalado, solicitale al usuario instalar uno:

- macOS: `brew install --cask google-chrome`
- Ubuntu/Debian: `sudo apt install chromium-browser`
