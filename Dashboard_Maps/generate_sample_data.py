#!/usr/bin/env python3
"""
Script para crear datos de ejemplo para el dashboard
Útil para testing sin los archivos reales
"""

import pandas as pd
import json
import random
from datetime import datetime, timedelta
import os

# Importar configuración
import sys
sys.path.insert(0, os.path.dirname(__file__))
from config import UBICACIONES_ARGENTINA, RUBROS_BUSQUEDA

def generar_csv_ejemplo(num_empresas=1000, output_path='data/ejemplo_google_maps_results.csv'):
    """Genera un CSV de ejemplo con empresas."""
    
    print(f"📝 Generando CSV de ejemplo con {num_empresas} empresas...")
    
    # Datos de ejemplo
    nombres_empresas = [
        "Fábrica Argentina S.A.", "Distribuidora del Sur", "Logística Express",
        "Industrias Unidas", "Comercial del Norte", "Servicios Integrales",
        "Construcciones Modernas", "Alimentaria Regional", "Textil Nacional",
        "Metalúrgica del Litoral", "Transporte Federal", "Tecnología Avanzada"
    ]
    
    categorias = [
        "Fábrica", "Distribuidor mayorista", "Empresa de logística",
        "Industria manufacturera", "Comercio mayorista", "Servicios empresariales",
        "Constructora", "Industria alimentaria", "Textil", "Metalúrgica",
        "Transporte de carga", "Empresa de tecnología"
    ]
    
    # Generar datos
    data = []
    
    for i in range(num_empresas):
        # Seleccionar ubicación aleatoria
        ubicacion_key = random.choice(list(UBICACIONES_ARGENTINA.keys()))
        ubicacion = UBICACIONES_ARGENTINA[ubicacion_key]
        
        # Generar coordenadas cercanas a la ubicación
        lat = ubicacion['lat'] + random.uniform(-0.5, 0.5)
        lng = ubicacion['lng'] + random.uniform(-0.5, 0.5)
        
        # Generar datos de la empresa
        empresa = {
            'nombre': f"{random.choice(nombres_empresas)} {i+1}",
            'direccion': f"Calle {random.randint(1, 100)} {random.randint(100, 9999)}",
            'ciudad': ubicacion['nombre'],
            'categoria': random.choice(categorias),
            'rating': round(random.uniform(3.0, 5.0), 1) if random.random() > 0.2 else None,
            'num_resenas': random.randint(0, 500) if random.random() > 0.2 else None,
            'telefono': f"+54 11 {random.randint(1000, 9999)}-{random.randint(1000, 9999)}" if random.random() > 0.3 else None,
            'sitio_web': f"www.empresa{i+1}.com.ar" if random.random() > 0.4 else None,
            'email': f"contacto@empresa{i+1}.com.ar" if random.random() > 0.5 else None,
            'url_google_maps': f"https://maps.google.com/?cid={random.randint(100000000, 999999999)}",
            'latitud': lat,
            'longitud': lng,
            'rubro_buscado': random.choice(RUBROS_BUSQUEDA),
            'segmento_id': random.randint(1, 100),
            'segmento_centro': f"{lat},{lng}",
            'fecha_extraccion': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d %H:%M:%S')
        }
        
        data.append(empresa)
    
    # Crear DataFrame y guardar
    df = pd.DataFrame(data)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    
    print(f"✅ CSV creado: {output_path}")
    print(f"   📊 {len(df)} empresas generadas")
    print(f"   🗺️  {df['ciudad'].nunique()} ubicaciones únicas")
    print(f"   🏷️  {df['rubro_buscado'].nunique()} rubros únicos")
    
    return df

def generar_json_estado(output_path='data/ejemplo_estado_ejecucion.json'):
    """Genera un JSON de estado de ejemplo."""
    
    print(f"\n📝 Generando JSON de estado de ejemplo...")
    
    estado = {
        "ubicaciones_completadas": {}
    }
    
    # Generar estado para algunas ubicaciones
    for ubicacion_key, ubicacion_data in list(UBICACIONES_ARGENTINA.items())[:15]:
        # Número aleatorio de rubros completados
        num_rubros = random.randint(50, len(RUBROS_BUSQUEDA))
        rubros_completados = random.sample(RUBROS_BUSQUEDA, num_rubros)
        
        estado["ubicaciones_completadas"][ubicacion_key] = {
            "nombre": ubicacion_data['nombre'],
            "rubros_completados": rubros_completados,
            "ultima_actualizacion": (datetime.now() - timedelta(days=random.randint(0, 5))).strftime('%Y-%m-%d %H:%M:%S')
        }
    
    # Guardar JSON
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(estado, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON creado: {output_path}")
    print(f"   📍 {len(estado['ubicaciones_completadas'])} ubicaciones procesadas")
    
    return estado

def main():
    """Función principal."""
    print("="*60)
    print("🧪 Generador de Datos de Ejemplo")
    print("="*60)
    print()
    
    # Generar CSV
    df = generar_csv_ejemplo(num_empresas=1000)
    
    # Generar JSON
    estado = generar_json_estado()
    
    print("\n" + "="*60)
    print("✅ Datos de ejemplo creados")
    print("="*60)
    print("\n💡 Para usar estos datos en el dashboard:")
    print("   1. Copia los archivos a las ubicaciones correctas, o")
    print("   2. Modifica las rutas en config.py para apuntar a estos archivos")
    print("\n⚠️  Estos son datos de prueba. Para datos reales, usa los archivos")
    print("   originales del scraping.")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
