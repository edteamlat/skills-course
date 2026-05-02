# Movies Finder - Guía de uso

Script en bash para consultar información de películas usando la API de [The Movie Database (TMDB)](https://www.themoviedb.org/).

## Requisitos

- `bash`
- `curl`
- `python3` (para codificar la query en el comando `search`)
- Token de acceso de TMDB ([obtenerlo aquí](https://www.themoviedb.org/settings/api))

## Comandos disponibles

| Comando    | Descripción                                      |
|------------|--------------------------------------------------|
| `search`   | Busca películas por texto                        |
| `discover` | Busca películas usando filtros avanzados         |
| `details`  | Obtiene los detalles de una película por ID TMDB |
| `find`     | Busca una película por ID externo (IMDB, etc.)   |

---

## search

Busca películas por su título (original, traducido o alternativo).

```bash
./movies.sh search --query <texto> [opciones]
```

### Opciones

| Opción                        | Descripción                          | Default  |
|-------------------------------|--------------------------------------|----------|
| `--query <texto>`             | Texto de búsqueda (requerido)        |          |
| `--language <lang>`           | Idioma de la respuesta               | `en-US`  |
| `--page <n>`                  | Número de página                     | `1`      |
| `--include-adult`             | Incluir contenido adulto             | `false`  |
| `--primary-release-year <año>`| Filtrar por año de estreno           |          |
| `--region <región>`           | Filtrar por región geográfica        |          |
| `--year <año>`                | Filtrar por año                      |          |

### Ejemplos

```bash
# Búsqueda simple
./movies.sh search --query "Jack Reacher"

# Con idioma español y página 2
./movies.sh search --query "Matrix" --language es-MX --page 2

# Filtrar por año de estreno
./movies.sh search --query "Spider-Man" --primary-release-year 2021

# Filtrar por región
./movies.sh search --query "Avengers" --region US
```

---

## discover

Busca películas usando filtros avanzados como género, puntuación, fechas, proveedores de streaming, etc.

```bash
./movies.sh discover [opciones]
```

### Opciones

| Opción                          | Descripción                                              | Default            |
|---------------------------------|----------------------------------------------------------|--------------------|
| `--language <lang>`             | Idioma de la respuesta                                   | `en-US`            |
| `--page <n>`                    | Número de página                                         | `1`                |
| `--sort-by <campo>`             | Campo de ordenamiento                                    | `popularity.desc`  |
| `--include-adult`               | Incluir contenido adulto                                 | `false`            |
| `--include-video`               | Incluir videos                                           | `false`            |
| `--region <región>`             | Región geográfica                                        |                    |
| `--primary-release-year <año>`  | Año de estreno principal                                 |                    |
| `--primary-release-date-gte`    | Fecha de estreno mínima (`YYYY-MM-DD`)                   |                    |
| `--primary-release-date-lte`    | Fecha de estreno máxima (`YYYY-MM-DD`)                   |                    |
| `--release-date-gte <fecha>`    | Fecha de lanzamiento mínima                              |                    |
| `--release-date-lte <fecha>`    | Fecha de lanzamiento máxima                              |                    |
| `--vote-average-gte <n>`        | Puntuación media mínima                                  |                    |
| `--vote-average-lte <n>`        | Puntuación media máxima                                  |                    |
| `--vote-count-gte <n>`          | Cantidad de votos mínima                                 |                    |
| `--vote-count-lte <n>`          | Cantidad de votos máxima                                 |                    |
| `--with-genres <ids>`           | IDs de géneros (coma o pipe separados)                   |                    |
| `--without-genres <ids>`        | Excluir géneros                                          |                    |
| `--with-cast <ids>`             | IDs de actores                                           |                    |
| `--with-crew <ids>`             | IDs de crew                                              |                    |
| `--with-people <ids>`           | IDs de personas (actores o crew)                         |                    |
| `--with-companies <ids>`        | IDs de productoras                                       |                    |
| `--without-companies <ids>`     | Excluir productoras                                      |                    |
| `--with-keywords <ids>`         | IDs de palabras clave                                    |                    |
| `--without-keywords <ids>`      | Excluir palabras clave                                   |                    |
| `--with-original-language`      | Idioma original de la película                           |                    |
| `--with-origin-country <país>`  | País de origen                                           |                    |
| `--with-release-type <1-6>`     | Tipo de lanzamiento                                      |                    |
| `--runtime-gte <min>`           | Duración mínima en minutos                               |                    |
| `--runtime-lte <min>`           | Duración máxima en minutos                               |                    |
| `--with-watch-providers <ids>`  | IDs de proveedores de streaming                          |                    |
| `--without-watch-providers`     | Excluir proveedores de streaming                         |                    |
| `--with-watch-types <tipos>`    | Tipos: `flatrate`, `free`, `ads`, `rent`, `buy`          |                    |
| `--watch-region <país>`         | Región para filtrar proveedores de streaming             |                    |
| `--certification <cert>`        | Certificación (usar con `--certification-country`)       |                    |
| `--certification-country <país>`| País de la certificación                                 |                    |
| `--cert-gte <cert>`             | Certificación mínima                                     |                    |
| `--cert-lte <cert>`             | Certificación máxima                                     |                    |
| `--year <año>`                  | Año                                                      |                    |

### Valores de `--sort-by`

`popularity.asc`, `popularity.desc`, `revenue.asc`, `revenue.desc`, `primary_release_date.asc`, `primary_release_date.desc`, `vote_average.asc`, `vote_average.desc`, `vote_count.asc`, `vote_count.desc`

### Ejemplos

```bash
# Películas de acción con alta puntuación
./movies.sh discover --with-genres 28 --vote-average-gte 8 --sort-by vote_average.desc

# Películas en español estrenadas en 2024
./movies.sh discover --with-original-language es --primary-release-year 2024

# Películas cortas (menos de 90 min) disponibles en Netflix (ID: 8)
./movies.sh discover --runtime-lte 90 --with-watch-providers 8 --watch-region US

# Películas de terror entre 2020 y 2023
./movies.sh discover --with-genres 27 --release-date-gte 2020-01-01 --release-date-lte 2023-12-31

# Películas con más de 1000 votos y puntuación entre 7 y 9
./movies.sh discover --vote-count-gte 1000 --vote-average-gte 7 --vote-average-lte 9
```

---

## details

Obtiene todos los detalles de una película usando su ID de TMDB. Soporta sub-requests adicionales con `--append`.

```bash
./movies.sh details --id <movie_id> [opciones]
```

### Opciones

| Opción               | Descripción                                   | Default  |
|----------------------|-----------------------------------------------|----------|
| `--id <movie_id>`    | ID de la película en TMDB (requerido)         |          |
| `--language <lang>`  | Idioma de la respuesta                        | `en-US`  |
| `--append <lista>`   | Sub-requests adicionales separados por coma   |          |

### Valores de `--append`

`videos`, `images`, `credits`, `keywords`, `recommendations`, `similar`, `reviews`, `release_dates`, `translations`, `external_ids`, `watch/providers`

### Ejemplos

```bash
# Detalles básicos de Star Wars (ID: 11)
./movies.sh details --id 11

# Detalles en español
./movies.sh details --id 11 --language es-MX

# Detalles con videos y créditos incluidos
./movies.sh details --id 11 --append videos,credits

# Detalles completos
./movies.sh details --id 343611 --append videos,images,credits,keywords,recommendations
```

---

## find

Busca una película usando un ID de una plataforma externa como IMDB, TVDB, etc.

```bash
./movies.sh find --id <external_id> --source <fuente> [opciones]
```

### Opciones

| Opción              | Descripción                      | Default  |
|---------------------|----------------------------------|----------|
| `--id <external_id>`| ID externo (requerido)           |          |
| `--source <fuente>` | Fuente del ID (requerido)        |          |
| `--language <lang>` | Idioma de la respuesta           | `en-US`  |

### Valores de `--source`

| Fuente          | Descripción              |
|-----------------|--------------------------|
| `imdb_id`       | ID de IMDB               |
| `tvdb_id`       | ID de TheTVDB            |
| `facebook_id`   | ID de Facebook           |
| `instagram_id`  | ID de Instagram          |
| `twitter_id`    | ID de Twitter/X          |
| `tiktok_id`     | ID de TikTok             |
| `wikidata_id`   | ID de Wikidata           |
| `youtube_id`    | ID de YouTube            |

### Ejemplos

```bash
# Buscar Interstellar por su ID de IMDB
./movies.sh find --id tt0816692 --source imdb_id

# Buscar The Matrix en español
./movies.sh find --id tt0133093 --source imdb_id --language es-MX

# Buscar por ID de Wikidata
./movies.sh find --id Q47703 --source wikidata_id
```

---

## Ayuda

Cada comando tiene su propio `--help`:

```bash
./movies.sh --help
./movies.sh search --help
./movies.sh discover --help
./movies.sh details --help
./movies.sh find --help
```
