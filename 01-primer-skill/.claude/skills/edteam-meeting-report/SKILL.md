---
name: edteam-meeting-report
description: >
  Genera reportes estructurados a partir de transcripciones de reuniones de EDteam.
  Úsalo SIEMPRE que el usuario mencione una transcripción, minuta, reunión, llamada,
  o pida resumir o reportar lo que se habló en una reunión. También actívalo cuando
  el usuario suba o pegue texto que parezca una transcripción (diálogos, nombres con
  dos puntos, timestamps). Produce tres secciones: descripción breve de la reunión,
  puntos clave en viñetas, y tareas/próximos pasos con responsables.
---

# EDteam Meeting Report

Genera un reporte limpio y accionable a partir de una transcripción de reunión.

## Fuentes de entrada soportadas

- Texto pegado directamente en el chat
- Archivos `.txt`, `.md`, `.pdf` subidos por el usuario
- Archivos en `/mnt/transcripts/` (directorio de transcripciones de EDteam)
- Transcripciones de Google Meet, Zoom, Loom, Fireflies, Otter, etc.

Si la fuente es un archivo, léelo primero con las herramientas disponibles antes de generar el reporte.

## Proceso

### 1. Leer la transcripción

- Si el usuario pegó el texto: úsalo directamente.
- Si hay un archivo adjunto o ruta: léelo con `bash_tool` o `view`.
- Si hay archivos en `/mnt/transcripts/` sin especificación: lista los disponibles y pregunta cuál procesar.

### 2. Generar el reporte

Produce las tres secciones siguientes **en español**, en ese orden exacto, con este formato:

---

## 📋 Descripción de la reunión

Un párrafo breve (3–5 oraciones) que incluya:
- Contexto o propósito de la reunión
- Participantes identificados (si están en la transcripción)
- Fecha/hora (si está disponible)
- Tema o proyecto principal tratado

---

## 🔑 Puntos clave

Lista de viñetas con los temas, decisiones o hallazgos más importantes discutidos.
- Sé concreto: menciona nombres de proyectos, funcionalidades, métricas o decisiones específicas.
- Ordena de mayor a menor relevancia.
- Entre 5 y 12 viñetas dependiendo de la extensión de la reunión.
- Evita redundancias; agrupa ideas relacionadas.

---

## ✅ Tareas y próximos pasos

Lista de viñetas, cada una con:
- **Qué** se debe hacer (acción concreta)
- **Quién** es responsable (nombre o rol; si no se menciona, indica "Sin asignar")
- **Cuándo** (fecha límite o referencia temporal si se mencionó)

Formato sugerido por viñeta:
`- **[Responsable]** — [Descripción de la tarea] *(fecha si aplica)*`

Si no hay tareas explícitas, indica: *"No se identificaron tareas concretas en esta reunión."*

---

### 3. Reglas de calidad

- **Idioma**: siempre español, incluso si la transcripción está en inglés o es bilingüe.
- **Fidelidad**: no inventes información; si algo es ambiguo, indícalo con *(no confirmado)*.
- **Brevedad**: el reporte debe poder leerse en 2 minutos. Evita párrafos largos fuera de la descripción.
- **Nombres propios**: preserva nombres de personas, proyectos y herramientas tal como aparecen.
- **Confidencialidad**: no reenvíes datos sensibles fuera del reporte (contraseñas, tokens, info financiera específica).

### 4. Entrega

- Muestra el reporte directamente en el chat con formato Markdown.
- Si el usuario pide un archivo, guárdalo como `.md` en `/mnt/user-data/outputs/` y preséntalo con `present_files`.
- Ofrece al final: *"¿Quieres que lo exporte como archivo o ajuste alguna sección?"*
