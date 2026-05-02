# CSV Contracts Analyzer

Analiza archivos CSV de contratos públicos (SECOP de Colombia) y genera tablas markdown.

## Script

```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /ruta/archivo.csv \
  '<opciones_json>'
```

## Parámetros JSON

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `top_n` | int | 5 | Número de registros |
| `sort_by` | str | "valor" | Campo: "valor", "entidad", "proceso" |
| `sort_desc` | bool | true | true = descendente, false = ascendente |
| `entidad_filter` | str | - | Filtrar por entidad |
| `tipo_filter` | str | - | Filtrar por tipo de contrato |
| `ciudad_filter` | str | - | Filtrar por ciudad |
| `valor_min` | int | - | Valor mínimo |
| `valor_max` | int | - | Valor máximo |

## Ejemplos

**Top 5 más costosos:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"top_n": 5}'
```

**Top 3 más económicos:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"top_n": 3, "sort_desc": false}'
```

**Contratos de Bogotá:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"ciudad_filter": "Bogotá", "top_n": 10}'
```

**Rango de valores:**
```bash
python /mnt/skills/user/csv-contracts-analyzer/scripts/analyzer.py \
  /mnt/user-data/uploads/export.csv \
  '{"valor_min": 10000000, "valor_max": 100000000}'
```

## Salida

Tabla markdown con 4 columnas:

| Entidad | Proceso | Valor (COP) | Link |
|---------|---------|-------------|------|
| SECRETARIA DE EDUCACION DEL DISTRITO | Caja Colombiana de Subsidio Familiar COLSUBSIDIO | $9.145.029.801 | https://community.secop.gov.co/... |
| GOBERNACION DEL HUILA | Prestación del servicio de alimentación escolar PAE | $8.896.957.990 | https://community.secop.gov.co/... |
| MUNICIPIO DE SOACHA | Mejoramiento y rehabilitación de vías urbanas | $8.545.073.975 | https://community.secop.gov.co/... |
