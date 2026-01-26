#!/usr/bin/env python3
"""
Script para descargar archivos GeoJSON de Argentina
Si los archivos no se pueden descargar, crea un GeoJSON simplificado de ejemplo
"""

import json
import os
import requests

# Crear directorio si no existe
DATA_DIR = "data/geo"
os.makedirs(DATA_DIR, exist_ok=True)

# URLs de fuentes para GeoJSON de Argentina
GEOJSON_URLS = {
    'provincias': [
        'https://raw.githubusercontent.com/southamerica-geojson/argentina-geojson/master/argentina-provincias.geojson',
        'https://raw.githubusercontent.com/argentina-geodata/provincias/master/provincias.geojson',
    ]
}

def descargar_geojson(nombre, urls):
    """Intenta descargar el GeoJSON desde las URLs proporcionadas."""
    output_path = os.path.join(DATA_DIR, f"argentina_{nombre}.geojson")
    
    print(f"\n📥 Descargando {nombre}...")
    
    for i, url in enumerate(urls, 1):
        try:
            print(f"   Intento {i}/{len(urls)}: {url}")
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Guardar archivo
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                
                print(f"   ✅ Descargado exitosamente: {output_path}")
                return True
                
        except Exception as e:
            print(f"   ❌ Error: {e}")
    
    print(f"   ⚠️  No se pudo descargar desde ninguna URL")
    return False

def crear_geojson_ejemplo():
    """Crea un GeoJSON simplificado de ejemplo para Argentina."""
    print("\n📝 Creando GeoJSON de ejemplo simplificado...")
    
    # GeoJSON simplificado con provincias principales
    geojson_ejemplo = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nombre": "Buenos Aires",
                    "id": "02",
                    "iso_id": "AR-B"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-58.5, -34.5], [-58.5, -36.5], [-61.5, -36.5], 
                        [-61.5, -34.5], [-58.5, -34.5]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nombre": "Ciudad Autónoma de Buenos Aires",
                    "id": "01",
                    "iso_id": "AR-C"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-58.3, -34.5], [-58.3, -34.7], [-58.5, -34.7],
                        [-58.5, -34.5], [-58.3, -34.5]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nombre": "Córdoba",
                    "id": "03",
                    "iso_id": "AR-X"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-64.0, -31.0], [-64.0, -33.0], [-66.0, -33.0],
                        [-66.0, -31.0], [-64.0, -31.0]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nombre": "Santa Fe",
                    "id": "04",
                    "iso_id": "AR-S"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-60.5, -28.0], [-60.5, -33.5], [-62.5, -33.5],
                        [-62.5, -28.0], [-60.5, -28.0]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nombre": "Mendoza",
                    "id": "05",
                    "iso_id": "AR-M"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-68.0, -32.5], [-68.0, -37.5], [-70.5, -37.5],
                        [-70.5, -32.5], [-68.0, -32.5]
                    ]]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "nombre": "Tucumán",
                    "id": "06",
                    "iso_id": "AR-T"
                },
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [[
                        [-65.0, -26.5], [-65.0, -28.0], [-66.5, -28.0],
                        [-66.5, -26.5], [-65.0, -26.5]
                    ]]
                }
            }
        ]
    }
    
    output_path = os.path.join(DATA_DIR, "argentina_provincias.geojson")
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(geojson_ejemplo, f, ensure_ascii=False, indent=2)
    
    print(f"   ✅ Creado archivo de ejemplo: {output_path}")
    print("   ⚠️  NOTA: Este es un GeoJSON simplificado con geometrías aproximadas")
    print("   💡 Para mapas de producción, descarga archivos oficiales desde:")
    print("      - https://www.ign.gob.ar/ (Instituto Geográfico Nacional)")
    print("      - https://www.indec.gob.ar/ (INDEC)")
    print("      - https://github.com/LatinGeo/argentina-geojson")

def main():
    """Función principal."""
    print("="*60)
    print("🗺️  Descargador de GeoJSON de Argentina")
    print("="*60)
    
    # Intentar descargar provincias
    exito = descargar_geojson('provincias', GEOJSON_URLS['provincias'])
    
    # Si no se pudo descargar, crear ejemplo
    if not exito:
        crear_geojson_ejemplo()
    
    print("\n" + "="*60)
    print("✅ Proceso completado")
    print("="*60)
    print(f"\nArchivos en: {os.path.abspath(DATA_DIR)}/")
    print("\n💡 Instrucciones adicionales:")
    print("   1. Los archivos GeoJSON están listos para usar en el dashboard")
    print("   2. Si usaste el archivo de ejemplo, considera descargar versiones")
    print("      oficiales para mayor precisión")
    print("   3. Puedes reemplazar los archivos en cualquier momento")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
