#!/usr/bin/env python3
"""
Utilidades adicionales para el scraper
Script con funciones útiles para mantenimiento y análisis
"""
import sys
import json
from pathlib import Path
import pandas as pd


def limpiar_todo():
    """Limpia todos los archivos generados y resetea el proyecto"""
    print("🧹 Limpiando archivos generados...")
    
    archivos_a_eliminar = [
        'estado_ejecucion.json',
        'cookies.pkl'
    ]
    
    directorios_a_limpiar = ['resultados', 'backups', 'logs']
    
    # Eliminar archivos
    for archivo in archivos_a_eliminar:
        path = Path(archivo)
        if path.exists():
            path.unlink()
            print(f"  ✅ Eliminado: {archivo}")
    
    # Limpiar directorios
    for directorio in directorios_a_limpiar:
        dir_path = Path(directorio)
        if dir_path.exists():
            for archivo in dir_path.iterdir():
                if archivo.is_file():
                    archivo.unlink()
            print(f"  ✅ Limpiado: {directorio}/")
    
    print("\n✅ Limpieza completada. El proyecto está listo para empezar de cero.")


def ver_estado():
    """Muestra el estado actual de la ejecución"""
    estado_file = Path('estado_ejecucion.json')
    
    if not estado_file.exists():
        print("ℹ️  No hay estado guardado. El scraper no ha sido ejecutado aún.")
        return
    
    try:
        with open(estado_file, 'r', encoding='utf-8') as f:
            estado = json.load(f)
        
        print("📊 Estado actual del scraper:")
        print(f"  Empresas extraídas: {estado.get('empresas_extraidas', 0)}")
        print(f"  Fecha de inicio: {estado.get('fecha_inicio', 'N/A')}")
        print(f"  Último checkpoint: {estado.get('ultimo_checkpoint', 'N/A')}")
        
        segmentos = estado.get('segmentos_completados', {})
        print(f"  Segmentos completados: {len(segmentos)}")
        
        if segmentos:
            print("\n  Detalle de segmentos:")
            for seg_id, seg_data in segmentos.items():
                rubros = seg_data.get('rubros', [])
                print(f"    - {seg_id}: {len(rubros)} rubros completados")
        
    except Exception as e:
        print(f"❌ Error leyendo estado: {e}")


def analizar_resultados():
    """Analiza los resultados obtenidos"""
    excel_file = Path('resultados/google_maps_results.xlsx')
    
    if not excel_file.exists():
        print("ℹ️  No hay resultados para analizar.")
        return
    
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        print("📊 Análisis de resultados:")
        print(f"  Total de lugares: {len(df)}")
        print()
        
        # Por rubro
        if 'rubro_buscado' in df.columns:
            print("  Lugares por rubro:")
            rubros = df['rubro_buscado'].value_counts()
            for rubro, count in rubros.items():
                print(f"    - {rubro}: {count}")
            print()
        
        # Con teléfono
        if 'telefono' in df.columns:
            con_telefono = df['telefono'].notna().sum()
            porcentaje = (con_telefono / len(df) * 100) if len(df) > 0 else 0
            print(f"  Con teléfono: {con_telefono} ({porcentaje:.1f}%)")
        
        # Con sitio web
        if 'sitio_web' in df.columns:
            con_web = df['sitio_web'].notna().sum()
            porcentaje = (con_web / len(df) * 100) if len(df) > 0 else 0
            print(f"  Con sitio web: {con_web} ({porcentaje:.1f}%)")
        
        # Rating promedio
        if 'rating' in df.columns:
            ratings_validos = pd.to_numeric(df['rating'], errors='coerce').dropna()
            if len(ratings_validos) > 0:
                rating_promedio = ratings_validos.mean()
                print(f"  Rating promedio: {rating_promedio:.2f}")
        
        print()
        
        # Ciudades más representadas
        if 'direccion' in df.columns:
            print("  Top 5 palabras en direcciones:")
            # Extraer palabras comunes de las direcciones
            todas_direcciones = ' '.join(df['direccion'].dropna().astype(str))
            palabras = todas_direcciones.split()
            from collections import Counter
            palabras_comunes = Counter(palabras).most_common(5)
            for palabra, count in palabras_comunes:
                if len(palabra) > 3:  # Filtrar palabras muy cortas
                    print(f"    - {palabra}: {count} veces")
        
    except Exception as e:
        print(f"❌ Error analizando resultados: {e}")


def exportar_csv():
    """Exporta los resultados de Excel a CSV"""
    excel_file = Path('resultados/google_maps_results.xlsx')
    csv_file = Path('resultados/google_maps_results.csv')
    
    if not excel_file.exists():
        print("ℹ️  No hay resultados para exportar.")
        return
    
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f"✅ Exportado a CSV: {csv_file}")
        print(f"   {len(df)} filas exportadas")
    except Exception as e:
        print(f"❌ Error exportando: {e}")


def filtrar_por_rubro(rubro):
    """Filtra resultados por un rubro específico"""
    excel_file = Path('resultados/google_maps_results.xlsx')
    
    if not excel_file.exists():
        print("ℹ️  No hay resultados para filtrar.")
        return
    
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        if 'rubro_buscado' not in df.columns:
            print("❌ La columna 'rubro_buscado' no existe.")
            return
        
        df_filtrado = df[df['rubro_buscado'] == rubro]
        
        if df_filtrado.empty:
            print(f"ℹ️  No se encontraron resultados para el rubro '{rubro}'")
            print(f"   Rubros disponibles: {', '.join(df['rubro_buscado'].unique())}")
            return
        
        output_file = Path(f'resultados/{rubro.replace(" ", "_")}.xlsx')
        df_filtrado.to_excel(output_file, index=False, engine='openpyxl')
        
        print(f"✅ Filtrado por rubro '{rubro}':")
        print(f"   {len(df_filtrado)} lugares encontrados")
        print(f"   Guardado en: {output_file}")
        
    except Exception as e:
        print(f"❌ Error filtrando: {e}")


def listar_rubros():
    """Lista todos los rubros en los resultados"""
    excel_file = Path('resultados/google_maps_results.xlsx')
    
    if not excel_file.exists():
        print("ℹ️  No hay resultados.")
        return
    
    try:
        df = pd.read_excel(excel_file, engine='openpyxl')
        
        if 'rubro_buscado' not in df.columns:
            print("❌ La columna 'rubro_buscado' no existe.")
            return
        
        rubros = df['rubro_buscado'].value_counts()
        
        print("📋 Rubros encontrados:")
        for rubro, count in rubros.items():
            print(f"  - {rubro}: {count} lugares")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def mostrar_menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*60)
    print("🛠️  UTILIDADES DEL SCRAPER DE GOOGLE MAPS")
    print("="*60)
    print()
    print("Opciones disponibles:")
    print("  1. Ver estado actual")
    print("  2. Analizar resultados")
    print("  3. Exportar a CSV")
    print("  4. Listar rubros")
    print("  5. Filtrar por rubro")
    print("  6. Limpiar todo (resetear proyecto)")
    print("  0. Salir")
    print()


def main():
    """Función principal"""
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == 'limpiar':
            limpiar_todo()
        elif comando == 'estado':
            ver_estado()
        elif comando == 'analizar':
            analizar_resultados()
        elif comando == 'csv':
            exportar_csv()
        elif comando == 'rubros':
            listar_rubros()
        elif comando == 'filtrar':
            if len(sys.argv) > 2:
                filtrar_por_rubro(sys.argv[2])
            else:
                print("❌ Debes especificar un rubro: python utils_cli.py filtrar 'nombre_rubro'")
        else:
            print(f"❌ Comando desconocido: {comando}")
            print()
            print("Comandos disponibles:")
            print("  python utils_cli.py estado    - Ver estado actual")
            print("  python utils_cli.py analizar  - Analizar resultados")
            print("  python utils_cli.py csv       - Exportar a CSV")
            print("  python utils_cli.py rubros    - Listar rubros")
            print("  python utils_cli.py filtrar 'rubro' - Filtrar por rubro")
            print("  python utils_cli.py limpiar   - Limpiar todo")
    else:
        # Modo interactivo
        while True:
            mostrar_menu()
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '0':
                print("\n👋 ¡Hasta luego!")
                break
            elif opcion == '1':
                print()
                ver_estado()
            elif opcion == '2':
                print()
                analizar_resultados()
            elif opcion == '3':
                print()
                exportar_csv()
            elif opcion == '4':
                print()
                listar_rubros()
            elif opcion == '5':
                print()
                rubro = input("Ingresa el nombre del rubro: ").strip()
                filtrar_por_rubro(rubro)
            elif opcion == '6':
                print()
                confirmacion = input("⚠️  ¿Estás seguro? Esto eliminará todos los datos (s/n): ").strip().lower()
                if confirmacion == 's':
                    limpiar_todo()
            else:
                print("\n❌ Opción inválida")
            
            input("\nPresiona Enter para continuar...")


if __name__ == "__main__":
    main()
