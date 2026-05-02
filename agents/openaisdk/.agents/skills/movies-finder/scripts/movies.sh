#!/usr/bin/env bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../../../.." && pwd)"
ENV_FILE="${PROJECT_ROOT}/.env"

if [[ ! -f "$ENV_FILE" ]]; then
  echo "Error: archivo .env no encontrado en $ENV_FILE" >&2
  echo "Crea uno basado en .env.example con tu TMDB_ACCESS_TOKEN" >&2
  exit 1
fi

# shellcheck source=.env
source "$ENV_FILE"

if [[ -z "${TMDB_ACCESS_TOKEN:-}" ]]; then
  echo "Error: TMDB_ACCESS_TOKEN no está definido en .env" >&2
  exit 1
fi

BASE_URL="https://api.themoviedb.org/3"
AUTH_HEADER="Authorization: Bearer ${TMDB_ACCESS_TOKEN}"

COUNTER_FILE="${SCRIPT_DIR}/../usage_count.txt"
count=0
[[ -f "$COUNTER_FILE" ]] && count=$(cat "$COUNTER_FILE")
echo $(( count + 1 )) > "$COUNTER_FILE"

usage() {
  cat <<EOF
Uso: $(basename "$0") <comando> [opciones]

Comandos:
  search      Buscar películas por texto
  discover    Buscar películas con filtros avanzados
  details     Obtener detalles de una película por su ID de TMDB
  find        Buscar por ID externo (IMDB, TVDB, etc.)

Ejecuta $(basename "$0") <comando> --help para ver las opciones de cada comando.
EOF
}

# ──────────────────────────────────────────────
# search
# ──────────────────────────────────────────────
cmd_search() {
  local query="" language="en-US" page=1 include_adult="false"
  local primary_release_year="" region="" year=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help|-h)
        cat <<EOF
Uso: $(basename "$0") search --query <texto> [opciones]

Opciones:
  --query <texto>                  Texto de búsqueda (requerido)
  --language <lang>                Idioma (default: en-US)
  --page <n>                       Página de resultados (default: 1)
  --include-adult                  Incluir contenido adulto
  --primary-release-year <año>     Filtrar por año de estreno
  --region <región>                Región geográfica
  --year <año>                     Filtrar por año
EOF
        return 0 ;;
      --query) query="$2"; shift 2 ;;
      --language) language="$2"; shift 2 ;;
      --page) page="$2"; shift 2 ;;
      --include-adult) include_adult="true"; shift ;;
      --primary-release-year) primary_release_year="$2"; shift 2 ;;
      --region) region="$2"; shift 2 ;;
      --year) year="$2"; shift 2 ;;
      *) echo "Opción desconocida: $1" >&2; return 1 ;;
    esac
  done

  if [[ -z "$query" ]]; then
    echo "Error: --query es requerido" >&2
    return 1
  fi

  local encoded_query
  encoded_query=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$query'))")

  local url="${BASE_URL}/search/movie?query=${encoded_query}&language=${language}&page=${page}&include_adult=${include_adult}"
  [[ -n "$primary_release_year" ]] && url+="&primary_release_year=${primary_release_year}"
  [[ -n "$region" ]]               && url+="&region=${region}"
  [[ -n "$year" ]]                 && url+="&year=${year}"

  curl --silent --request GET \
       --url "$url" \
       --header "$AUTH_HEADER" \
       --header "accept: application/json"
}

# ──────────────────────────────────────────────
# discover
# ──────────────────────────────────────────────
cmd_discover() {
  local language="en-US" page=1 include_adult="false" include_video="false"
  local sort_by="popularity.desc" region="" certification="" certification_country=""
  local cert_gte="" cert_lte="" primary_release_year="" prd_gte="" prd_lte=""
  local rd_gte="" rd_lte="" vote_avg_gte="" vote_avg_lte="" vote_count_gte="" vote_count_lte=""
  local with_cast="" with_companies="" with_crew="" with_genres="" with_keywords=""
  local with_origin_country="" with_original_language="" with_people="" with_release_type=""
  local runtime_gte="" runtime_lte="" with_watch_types="" with_watch_providers=""
  local without_companies="" without_genres="" without_keywords="" without_watch_providers=""
  local watch_region="" year=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help|-h)
        cat <<EOF
Uso: $(basename "$0") discover [opciones]

Opciones (todas opcionales):
  --language <lang>                    Idioma (default: en-US)
  --page <n>                           Página (default: 1)
  --sort-by <campo>                    Orden (default: popularity.desc)
  --include-adult                      Incluir contenido adulto
  --include-video                      Incluir videos
  --region <región>                    Región geográfica
  --certification <cert>               Certificación (usar con --certification-country)
  --certification-country <país>       País de certificación
  --cert-gte <cert>                    Certificación mínima
  --cert-lte <cert>                    Certificación máxima
  --primary-release-year <año>         Año de estreno principal
  --primary-release-date-gte <fecha>   Fecha de estreno mínima (YYYY-MM-DD)
  --primary-release-date-lte <fecha>   Fecha de estreno máxima (YYYY-MM-DD)
  --release-date-gte <fecha>           Fecha de lanzamiento mínima
  --release-date-lte <fecha>           Fecha de lanzamiento máxima
  --vote-average-gte <n>               Puntuación media mínima
  --vote-average-lte <n>               Puntuación media máxima
  --vote-count-gte <n>                 Cantidad de votos mínima
  --vote-count-lte <n>                 Cantidad de votos máxima
  --with-cast <ids>                    IDs de actores (coma/pipe separados)
  --with-companies <ids>               IDs de productoras
  --with-crew <ids>                    IDs de crew
  --with-genres <ids>                  IDs de géneros
  --with-keywords <ids>                IDs de palabras clave
  --with-origin-country <país>         País de origen
  --with-original-language <lang>      Idioma original
  --with-people <ids>                  IDs de personas
  --with-release-type <1-6>            Tipo de lanzamiento
  --runtime-gte <min>                  Duración mínima (minutos)
  --runtime-lte <min>                  Duración máxima (minutos)
  --with-watch-types <tipos>           Tipos: flatrate,free,ads,rent,buy
  --with-watch-providers <ids>         IDs de proveedores de streaming
  --watch-region <país>                Región para proveedores de streaming
  --without-companies <ids>            Excluir productoras
  --without-genres <ids>               Excluir géneros
  --without-keywords <ids>             Excluir palabras clave
  --without-watch-providers <ids>      Excluir proveedores
  --year <año>                         Año
EOF
        return 0 ;;
      --language) language="$2"; shift 2 ;;
      --page) page="$2"; shift 2 ;;
      --sort-by) sort_by="$2"; shift 2 ;;
      --include-adult) include_adult="true"; shift ;;
      --include-video) include_video="true"; shift ;;
      --region) region="$2"; shift 2 ;;
      --certification) certification="$2"; shift 2 ;;
      --certification-country) certification_country="$2"; shift 2 ;;
      --cert-gte) cert_gte="$2"; shift 2 ;;
      --cert-lte) cert_lte="$2"; shift 2 ;;
      --primary-release-year) primary_release_year="$2"; shift 2 ;;
      --primary-release-date-gte) prd_gte="$2"; shift 2 ;;
      --primary-release-date-lte) prd_lte="$2"; shift 2 ;;
      --release-date-gte) rd_gte="$2"; shift 2 ;;
      --release-date-lte) rd_lte="$2"; shift 2 ;;
      --vote-average-gte) vote_avg_gte="$2"; shift 2 ;;
      --vote-average-lte) vote_avg_lte="$2"; shift 2 ;;
      --vote-count-gte) vote_count_gte="$2"; shift 2 ;;
      --vote-count-lte) vote_count_lte="$2"; shift 2 ;;
      --with-cast) with_cast="$2"; shift 2 ;;
      --with-companies) with_companies="$2"; shift 2 ;;
      --with-crew) with_crew="$2"; shift 2 ;;
      --with-genres) with_genres="$2"; shift 2 ;;
      --with-keywords) with_keywords="$2"; shift 2 ;;
      --with-origin-country) with_origin_country="$2"; shift 2 ;;
      --with-original-language) with_original_language="$2"; shift 2 ;;
      --with-people) with_people="$2"; shift 2 ;;
      --with-release-type) with_release_type="$2"; shift 2 ;;
      --runtime-gte) runtime_gte="$2"; shift 2 ;;
      --runtime-lte) runtime_lte="$2"; shift 2 ;;
      --with-watch-types) with_watch_types="$2"; shift 2 ;;
      --with-watch-providers) with_watch_providers="$2"; shift 2 ;;
      --watch-region) watch_region="$2"; shift 2 ;;
      --without-companies) without_companies="$2"; shift 2 ;;
      --without-genres) without_genres="$2"; shift 2 ;;
      --without-keywords) without_keywords="$2"; shift 2 ;;
      --without-watch-providers) without_watch_providers="$2"; shift 2 ;;
      --year) year="$2"; shift 2 ;;
      *) echo "Opción desconocida: $1" >&2; return 1 ;;
    esac
  done

  local url="${BASE_URL}/discover/movie?language=${language}&page=${page}&sort_by=${sort_by}&include_adult=${include_adult}&include_video=${include_video}"

  [[ -n "$region" ]]               && url+="&region=${region}"
  [[ -n "$certification" ]]        && url+="&certification=${certification}"
  [[ -n "$certification_country" ]] && url+="&certification_country=${certification_country}"
  [[ -n "$cert_gte" ]]             && url+="&certification.gte=${cert_gte}"
  [[ -n "$cert_lte" ]]             && url+="&certification.lte=${cert_lte}"
  [[ -n "$primary_release_year" ]] && url+="&primary_release_year=${primary_release_year}"
  [[ -n "$prd_gte" ]]              && url+="&primary_release_date.gte=${prd_gte}"
  [[ -n "$prd_lte" ]]              && url+="&primary_release_date.lte=${prd_lte}"
  [[ -n "$rd_gte" ]]               && url+="&release_date.gte=${rd_gte}"
  [[ -n "$rd_lte" ]]               && url+="&release_date.lte=${rd_lte}"
  [[ -n "$vote_avg_gte" ]]         && url+="&vote_average.gte=${vote_avg_gte}"
  [[ -n "$vote_avg_lte" ]]         && url+="&vote_average.lte=${vote_avg_lte}"
  [[ -n "$vote_count_gte" ]]       && url+="&vote_count.gte=${vote_count_gte}"
  [[ -n "$vote_count_lte" ]]       && url+="&vote_count.lte=${vote_count_lte}"
  [[ -n "$with_cast" ]]            && url+="&with_cast=${with_cast}"
  [[ -n "$with_companies" ]]       && url+="&with_companies=${with_companies}"
  [[ -n "$with_crew" ]]            && url+="&with_crew=${with_crew}"
  [[ -n "$with_genres" ]]          && url+="&with_genres=${with_genres}"
  [[ -n "$with_keywords" ]]        && url+="&with_keywords=${with_keywords}"
  [[ -n "$with_origin_country" ]]  && url+="&with_origin_country=${with_origin_country}"
  [[ -n "$with_original_language" ]] && url+="&with_original_language=${with_original_language}"
  [[ -n "$with_people" ]]          && url+="&with_people=${with_people}"
  [[ -n "$with_release_type" ]]    && url+="&with_release_type=${with_release_type}"
  [[ -n "$runtime_gte" ]]          && url+="&with_runtime.gte=${runtime_gte}"
  [[ -n "$runtime_lte" ]]          && url+="&with_runtime.lte=${runtime_lte}"
  [[ -n "$with_watch_types" ]]     && url+="&with_watch_monetization_types=${with_watch_types}"
  [[ -n "$with_watch_providers" ]] && url+="&with_watch_providers=${with_watch_providers}"
  [[ -n "$watch_region" ]]         && url+="&watch_region=${watch_region}"
  [[ -n "$without_companies" ]]    && url+="&without_companies=${without_companies}"
  [[ -n "$without_genres" ]]       && url+="&without_genres=${without_genres}"
  [[ -n "$without_keywords" ]]     && url+="&without_keywords=${without_keywords}"
  [[ -n "$without_watch_providers" ]] && url+="&without_watch_providers=${without_watch_providers}"
  [[ -n "$year" ]]                 && url+="&year=${year}"

  curl --silent --request GET \
       --url "$url" \
       --header "$AUTH_HEADER" \
       --header "accept: application/json"
}

# ──────────────────────────────────────────────
# details
# ──────────────────────────────────────────────
cmd_details() {
  local movie_id="" language="en-US" append_to_response=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help|-h)
        cat <<EOF
Uso: $(basename "$0") details --id <movie_id> [opciones]

Opciones:
  --id <movie_id>              ID de la película en TMDB (requerido)
  --language <lang>            Idioma (default: en-US)
  --append <endpoints>         Sub-requests adicionales separados por coma
                               Ej: videos,images,credits,keywords,recommendations
EOF
        return 0 ;;
      --id) movie_id="$2"; shift 2 ;;
      --language) language="$2"; shift 2 ;;
      --append) append_to_response="$2"; shift 2 ;;
      *) echo "Opción desconocida: $1" >&2; return 1 ;;
    esac
  done

  if [[ -z "$movie_id" ]]; then
    echo "Error: --id es requerido" >&2
    return 1
  fi

  local url="${BASE_URL}/movie/${movie_id}?language=${language}"
  [[ -n "$append_to_response" ]] && url+="&append_to_response=${append_to_response}"

  curl --silent --request GET \
       --url "$url" \
       --header "$AUTH_HEADER" \
       --header "accept: application/json"
}

# ──────────────────────────────────────────────
# find
# ──────────────────────────────────────────────
cmd_find() {
  local external_id="" external_source="" language="en-US"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --help|-h)
        cat <<EOF
Uso: $(basename "$0") find --id <external_id> --source <external_source> [opciones]

Opciones:
  --id <external_id>       ID externo (requerido)
  --source <fuente>        Fuente del ID (requerido)
                           Valores: imdb_id, facebook_id, instagram_id,
                                    tvdb_id, tiktok_id, twitter_id,
                                    wikidata_id, youtube_id
  --language <lang>        Idioma (default: en-US)
EOF
        return 0 ;;
      --id) external_id="$2"; shift 2 ;;
      --source) external_source="$2"; shift 2 ;;
      --language) language="$2"; shift 2 ;;
      *) echo "Opción desconocida: $1" >&2; return 1 ;;
    esac
  done

  if [[ -z "$external_id" ]]; then
    echo "Error: --id es requerido" >&2
    return 1
  fi

  if [[ -z "$external_source" ]]; then
    echo "Error: --source es requerido" >&2
    return 1
  fi

  curl --silent --request GET \
       --url "${BASE_URL}/find/${external_id}?external_source=${external_source}&language=${language}" \
       --header "$AUTH_HEADER" \
       --header "accept: application/json"
}

# ──────────────────────────────────────────────
# main
# ──────────────────────────────────────────────
if [[ $# -eq 0 ]]; then
  usage
  exit 0
fi

COMMAND="$1"
shift

case "$COMMAND" in
  search)   cmd_search "$@" ;;
  discover) cmd_discover "$@" ;;
  details)  cmd_details "$@" ;;
  find)     cmd_find "$@" ;;
  --help|-h) usage ;;
  *) echo "Comando desconocido: $COMMAND" >&2; usage; exit 1 ;;
esac
