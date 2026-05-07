---
name: movies-finder
description: Busca y consulta información de películas usando la API de TMDB (The Movie Database). Usa esta skill cuando el usuario quiera buscar películas por título, filtrar por género, año, puntuación o idioma, obtener detalles completos de una película, buscar por ID externo como IMDB, o descubrir películas con criterios avanzados. Actívate también cuando el usuario mencione "buscar película", "información de película", "filtrar películas", "buscar en TMDB", "buscar por IMDB" o cuando quiera explorar el catálogo de películas con cualquier criterio.
---

# Movies Finder

Skill para consultar información de películas usando el script `movies.sh` que se comunica con la API de TMDB vía `curl`.

## Antes de empezar

### 1. Configurar el token de TMDB

El script requiere el archivo `.env` en la **raíz del proyecto** con el token de acceso a la API de TMDB.

Verifica si ya existe:
```bash
cat .env
```

Si no existe, créalo a partir del ejemplo incluido:
```bash
cp .env.example .env
# Luego edita .env y reemplaza el valor de TMDB_ACCESS_TOKEN
```

El token se obtiene en: https://www.themoviedb.org/settings/api (campo "API Read Access Token").

### 2. Ejecutar el script

El script está en `scripts/movies.sh` dentro de la skill. Ejecútalo siempre desde el directorio raíz del proyecto apuntando a su ruta relativa:

```bash
bash movies-finder/scripts/movies.sh <comando> [opciones]
```

> Para la referencia completa de todos los parámetros, lee: `references/how-to-use-movies-finder.md`

---

## Casos de uso básicos

### 1. Buscar una película por título

Cuando el usuario dice: *"busca la película Matrix"*, *"encuentra películas de Star Wars"*

```bash
bash movies-finder/scripts/movies.sh search --query "Matrix"
```

Con idioma en español:
```bash
bash movies-finder/scripts/movies.sh search --query "Matrix" --language es-MX
```

El resultado es un JSON con el array `results`. Cada elemento incluye `id`, `title`, `release_date`, `vote_average` y `overview`.

---

### 2. Obtener detalles de una película

Cuando el usuario dice: *"dame los detalles de la película con ID 603"*, *"quiero ver los créditos y videos de Interstellar"*

Primero busca el ID con `search`, luego:
```bash
bash movies-finder/scripts/movies.sh details --id 603
```

Con videos y créditos incluidos:
```bash
bash movies-finder/scripts/movies.sh details --id 157336 --append videos,credits
```

Opciones comunes de `--append`: `videos`, `images`, `credits`, `keywords`, `recommendations`, `similar`, `reviews`

---

### 3. Descubrir películas con filtros

Cuando el usuario dice: *"películas de acción con puntuación mayor a 8"*, *"comedias en español de 2023"*, *"películas disponibles en Netflix"*

```bash
# Acción (género 28) bien puntuadas
bash movies-finder/scripts/movies.sh discover \
  --with-genres 28 --vote-average-gte 8 --sort-by vote_average.desc

# Películas en español de 2024
bash movies-finder/scripts/movies.sh discover \
  --with-original-language es --primary-release-year 2024

# Disponibles en Netflix (ID 8) en México
bash movies-finder/scripts/movies.sh discover \
  --with-watch-providers 8 --watch-region MX --with-watch-types flatrate
```

IDs de géneros frecuentes: Acción=28, Comedia=35, Drama=18, Terror=27, Ciencia ficción=878, Animación=16, Romance=10749

---

### 4. Buscar por ID externo (IMDB, etc.)

Cuando el usuario dice: *"busca la película con ID de IMDB tt0816692"*, *"encuentra esta película de IMDB"*

```bash
bash movies-finder/scripts/movies.sh find \
  --id tt0816692 --source imdb_id
```

Fuentes disponibles: `imdb_id`, `tvdb_id`, `facebook_id`, `instagram_id`, `twitter_id`, `tiktok_id`, `wikidata_id`, `youtube_id`

---

## Flujo recomendado

Para la mayoría de consultas, el flujo natural es:

1. **Buscar** con `search` para obtener el `id` de la película
2. **Detallar** con `details --id <id> --append credits` para obtener toda la información incluyendo el reparto
3. Si el usuario quiere explorar sin un título específico, usar `discover` con los filtros que mencione

## Entrega de resultados

Los resultados siempre van en JSON. Este json lo utilizará otra skill para encargarse del proceso de reporte en pdf.
