#!/usr/bin/env python3
"""
CSV Contracts Analyzer - Script para procesar archivos CSV de contratos públicos
Genera una tabla markdown con los contratos solicitados por el usuario
"""

import csv
import re
import sys
import json
from pathlib import Path
from typing import List, Dict, Optional

class ContractAnalyzer:
    def __init__(self, csv_path: str):
        """Inicializa el analizador con un archivo CSV"""
        self.csv_path = csv_path
        self.contracts = []
        self.column_mapping = {}
        self._load_csv()
    
    def _load_csv(self):
        """Carga y procesa el archivo CSV"""
        try:
            with open(self.csv_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                
                # Detectar columnas
                if reader.fieldnames:
                    self._detect_columns(reader.fieldnames)
                
                # Procesar filas
                for row in reader:
                    contract = self._process_row(row)
                    if contract and contract['valor'] > 0:
                        self.contracts.append(contract)
        except Exception as e:
            raise Exception(f"Error al leer CSV: {str(e)}")
    
    def _detect_columns(self, fieldnames: List[str]):
        """Detecta automáticamente las columnas relevantes"""
        fieldnames_lower = [f.lower() for f in fieldnames]
        
        # Mapeo de posibles nombres de columnas
        mappings = {
            'entidad': ['entidad', 'entity', 'institution', 'nombre entidad'],
            'proceso': ['nombre del procedimiento', 'procedimiento', 'proceso', 'nombre proceso', 'description'],
            'valor': ['precio base', 'valor', 'price', 'amount', 'monto', 'valor total adjudicacion'],
            'link': ['urlproceso', 'url', 'link', 'enlace', 'url proceso'],
            'ciudad': ['ciudad entidad', 'ciudad', 'city', 'municipio'],
            'tipo': ['tipo de contrato', 'tipo contrato', 'contract type', 'tipo']
        }
        
        for key, possible_names in mappings.items():
            for field_lower in fieldnames_lower:
                for possible_name in possible_names:
                    if possible_name in field_lower:
                        # Encontrar el nombre original (con mayúsculas)
                        original_name = fieldnames[fieldnames_lower.index(field_lower)]
                        self.column_mapping[key] = original_name
                        break
                if key in self.column_mapping:
                    break
    
    def _clean_value(self, value_str: str) -> int:
        """Convierte un valor monetario formateado a entero"""
        if not value_str or not isinstance(value_str, str):
            return 0
        # Remover $, espacios, y comas
        cleaned = re.sub(r'[^\d]', '', value_str.strip())
        try:
            return int(cleaned) if cleaned else 0
        except ValueError:
            return 0
    
    def _format_currency(self, value: int) -> str:
        """Formatea un número como moneda con separador de miles"""
        return f"${value:,}".replace(',', '.')  # Usar . como separador de miles (formato colombiano)
    
    def _process_row(self, row: Dict[str, str]) -> Optional[Dict]:
        """Procesa una fila del CSV"""
        try:
            entidad = row.get(self.column_mapping.get('entidad', ''), 'N/A').strip()
            proceso = row.get(self.column_mapping.get('proceso', ''), 'N/A').strip()
            valor_str = row.get(self.column_mapping.get('valor', ''), '0')
            link = row.get(self.column_mapping.get('link', ''), 'N/A').strip()
            ciudad = row.get(self.column_mapping.get('ciudad', ''), 'N/A').strip()
            tipo = row.get(self.column_mapping.get('tipo', ''), 'N/A').strip()
            
            valor = self._clean_value(valor_str)
            
            if valor > 0 and entidad != 'N/A':
                return {
                    'entidad': entidad,
                    'proceso': proceso,
                    'valor': valor,
                    'valor_formateado': self._format_currency(valor),
                    'link': link,
                    'ciudad': ciudad,
                    'tipo': tipo
                }
        except Exception:
            pass
        
        return None
    
    def filter_contracts(self, 
                        entidad_filter: Optional[str] = None,
                        tipo_filter: Optional[str] = None,
                        ciudad_filter: Optional[str] = None,
                        valor_min: Optional[int] = None,
                        valor_max: Optional[int] = None) -> List[Dict]:
        """Filtra contratos según criterios"""
        filtered = self.contracts
        
        if entidad_filter:
            entidad_lower = entidad_filter.lower()
            filtered = [c for c in filtered if entidad_lower in c['entidad'].lower()]
        
        if tipo_filter:
            tipo_lower = tipo_filter.lower()
            filtered = [c for c in filtered if tipo_lower in c['tipo'].lower()]
        
        if ciudad_filter:
            ciudad_lower = ciudad_filter.lower()
            filtered = [c for c in filtered if ciudad_lower in c['ciudad'].lower()]
        
        if valor_min is not None:
            filtered = [c for c in filtered if c['valor'] >= valor_min]
        
        if valor_max is not None:
            filtered = [c for c in filtered if c['valor'] <= valor_max]
        
        return filtered
    
    def sort_contracts(self, contracts: List[Dict], 
                      sort_by: str = 'valor',
                      descending: bool = True) -> List[Dict]:
        """Ordena contratos según criterios"""
        reverse = descending
        
        if sort_by == 'valor':
            return sorted(contracts, key=lambda x: x['valor'], reverse=reverse)
        elif sort_by == 'entidad':
            return sorted(contracts, key=lambda x: x['entidad'], reverse=reverse)
        elif sort_by == 'proceso':
            return sorted(contracts, key=lambda x: x['proceso'], reverse=reverse)
        
        return contracts
    
    def get_top_n(self, n: int = 5,
                  sort_by: str = 'valor',
                  descending: bool = True,
                  entidad_filter: Optional[str] = None,
                  tipo_filter: Optional[str] = None,
                  ciudad_filter: Optional[str] = None,
                  valor_min: Optional[int] = None,
                  valor_max: Optional[int] = None) -> List[Dict]:
        """Obtiene los Top N contratos con filtros y ordenamiento"""
        # Aplicar filtros
        filtered = self.filter_contracts(
            entidad_filter=entidad_filter,
            tipo_filter=tipo_filter,
            ciudad_filter=ciudad_filter,
            valor_min=valor_min,
            valor_max=valor_max
        )
        
        # Ordenar
        sorted_contracts = self.sort_contracts(filtered, sort_by, descending)
        
        # Obtener Top N
        return sorted_contracts[:n]
    
    def to_markdown_table(self, contracts: List[Dict]) -> str:
        """Convierte una lista de contratos a tabla markdown"""
        if not contracts:
            return "No se encontraron contratos que coincidan con los criterios."
        
        # Header
        markdown = "| Entidad | Proceso | Valor (COP) | Link |\n"
        markdown += "|---------|---------|-------------|------|\n"
        
        # Filas
        for contract in contracts:
            entidad = contract['entidad'][:40] + '...' if len(contract['entidad']) > 40 else contract['entidad']
            proceso = contract['proceso'][:50] + '...' if len(contract['proceso']) > 50 else contract['proceso']
            valor = contract['valor_formateado']
            link = contract['link'][:30] + '...' if len(contract['link']) > 30 else contract['link']
            
            # Escapar caracteres especiales para markdown
            entidad = entidad.replace('|', '\\|')
            proceso = proceso.replace('|', '\\|')
            
            markdown += f"| {entidad} | {proceso} | {valor} | {link} |\n"
        
        return markdown

def main():
    """Función principal para uso desde línea de comandos"""
    if len(sys.argv) < 2:
        print("Uso: python analyzer.py <csv_path> [options]")
        return
    
    csv_path = sys.argv[1]
    
    # Parse options from JSON si existen
    options = {}
    if len(sys.argv) > 2:
        try:
            options = json.loads(sys.argv[2])
        except json.JSONDecodeError:
            pass
    
    # Crear analizador
    analyzer = ContractAnalyzer(csv_path)
    
    # Obtener configuración
    top_n = options.get('top_n', 5)
    sort_by = options.get('sort_by', 'valor')
    sort_desc = options.get('sort_desc', True)
    entidad = options.get('entidad_filter')
    tipo = options.get('tipo_filter')
    ciudad = options.get('ciudad_filter')
    valor_min = options.get('valor_min')
    valor_max = options.get('valor_max')
    
    # Obtener contratos
    contracts = analyzer.get_top_n(
        n=top_n,
        sort_by=sort_by,
        descending=sort_desc,
        entidad_filter=entidad,
        tipo_filter=tipo,
        ciudad_filter=ciudad,
        valor_min=valor_min,
        valor_max=valor_max
    )
    
    # Generar markdown
    markdown = analyzer.to_markdown_table(contracts)
    
    # Imprimir resultado
    print(markdown)

if __name__ == '__main__':
    main()
