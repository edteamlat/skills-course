---
name: csv-contracts-analyzer
description: Analiza archivos CSV de contratos públicos (SECOP de Colombia). Filtra, ordena y extrae N contratos más costosos o económicos con opciones de filtro por entidad, tipo, ciudad y rango de valores.
---

# CSV Contracts Analyzer

Procesa archivos CSV de contratos públicos y genera tablas markdown.

## Cuándo usar

- Usuario carga un CSV de contratos públicos
- Solicita "Top N más costosos/económicos" o contratos filtrados

## Cómo usar

### Script
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /ruta/archivo.csv \
  '<opciones_json>'
```

### Opciones (JSON)

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `top_n` | int | 5 | Número de registros a retornar |
| `sort_by` | str | "valor" | Campo para ordenar: "valor", "entidad", "proceso" |
| `sort_desc` | bool | true | true = descendente (costosos), false = ascendente (económicos) |
| `entidad_filter` | str | - | Filtrar por nombre de entidad (búsqueda parcial) |
| `tipo_filter` | str | - | Filtrar por tipo de contrato |
| `ciudad_filter` | str | - | Filtrar por ciudad |
| `valor_min` | int | - | Valor mínimo |
| `valor_max` | int | - | Valor máximo |

### Ejemplos

**Top 5 más costosos:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"top_n": 5, "sort_by": "valor", "sort_desc": true}'
```

**Top 3 más económicos:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"top_n": 3, "sort_by": "valor", "sort_desc": false}'
```

**Contratos de Bogotá, ordenados por entidad:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"top_n": 10, "sort_by": "entidad", "ciudad_filter": "Bogotá"}'
```

**Contratos entre 10M y 100M:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"top_n": 5, "valor_min": 10000000, "valor_max": 100000000}'
```

## Salida

Tabla markdown con 4 columnas:

| Entidad | Proceso | Valor (COP) | Link |
|---------|---------|-------------:|------|
| SECRETARIA DE EDUCACION DEL DISTRITO | CO1.REQ.1928260 | $9.145.029.801 | https://community.secop.gov.co/... |
| GOBERNACION DEL HUILA | CO1.REQ.192826 | $8.896.957.990 | https://community.secop.gov.co/... |
| MUNICIPIO DE SOACHA | CO1.REQ.1921221 | $8.545.073.975 | https://community.secop.gov.co/... |
