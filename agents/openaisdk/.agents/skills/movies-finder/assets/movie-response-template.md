# Template de respuesta: detalle de una película

Usa este formato cada vez que presentes los detalles de una película.

---

## Formato

```
🎬 **{Título}** ({año})
⭐ {puntuación}/10  ·  🗓️ {DD de mes de AAAA}  ·  ⏱️ {Xh Xmin}

**Géneros:** {Género1}, {Género2}, {Género3}

**Protagonistas:** {Actor1}, {Actor2}, {Actor3} *(y N más)*

---
**Sinopsis**
{Texto de la sinopsis.}
```

---

## Reglas de llenado

| Campo | Fuente en la API | Notas |
|---|---|---|
| Título | `title` | — |
| Año | `release_date` (AAAA-MM-DD) | Solo el año, entre paréntesis |
| Puntuación | `vote_average` | Redondear a 1 decimal |
| Fecha de estreno | `release_date` | Formato: "5 de noviembre de 2014" |
| Duración | `runtime` (minutos) | Convertir a Xh Xmin; omitir si no está disponible |
| Géneros | `genres[].name` | Separados por coma |
| Protagonistas | `credits.cast` ordenado por `order` | Primeros 3–5; indicar cuántos más hay |
| Sinopsis | `overview` | Si está vacía, escribir *"Sin sinopsis disponible."* |

**Meses en español:** enero · febrero · marzo · abril · mayo · junio · julio · agosto · septiembre · octubre · noviembre · diciembre

> Para obtener `credits`, ejecuta el script con `--append credits`:
> ```bash
> bash .claude/skills/movies-finder/scripts/movies.sh details --id {id} --append credits
> ```

---

## Ejemplo

```
🎬 **Interestelar** (2014)
⭐ 8.4/10  ·  🗓️ 5 de noviembre de 2014  ·  ⏱️ 2h 49min

**Géneros:** Aventura, Drama, Ciencia ficción

**Protagonistas:** Matthew McConaughey, Anne Hathaway, Jessica Chastain *(y 47 más)*

---
**Sinopsis**
Un grupo de exploradores viaja a través de un agujero de gusano en el espacio en busca de un nuevo hogar para la humanidad, enfrentando los límites del tiempo y el espacio.
```

---

## Múltiples resultados

Cuando la búsqueda devuelve más de un resultado, primero muestra una lista resumida y luego aplica el template completo al más relevante (o al que elija el usuario):

```
Encontré varias películas para "{consulta}":

1. **{Título 1}** ({año}) — ⭐ {puntuación}
2. **{Título 2}** ({año}) — ⭐ {puntuación}
3. **{Título 3}** ({año}) — ⭐ {puntuación}

Mostrando detalles de la más relevante:

🎬 **{Título}** ({año})
...
```
