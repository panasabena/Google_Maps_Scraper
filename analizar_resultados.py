#!/usr/bin/env python3
"""
Script de análisis y visualización de resultados
Genera reportes y estadísticas de los datos extraídos
"""
import sys
from pathlib import Path
import pandas as pd
import json
from datetime import datetime


class ResultadosAnalyzer:
    def __init__(self, archivo_excel='resultados/google_maps_results.xlsx'):
        self.archivo_excel = Path(archivo_excel)
        self.df = None
        
    def cargar_datos(self):
        """Carga los datos del archivo Excel"""
        if not self.archivo_excel.exists():
            print(f"❌ No se encontró el archivo: {self.archivo_excel}")
            return False
        
        try:
            self.df = pd.read_excel(self.archivo_excel, engine='openpyxl')
            print(f"✅ Datos cargados: {len(self.df)} registros")
            return True
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            return False
    
    def generar_reporte_completo(self):
        """Genera un reporte completo de los resultados"""
        if self.df is None or self.df.empty:
            print("No hay datos para analizar")
            return
        
        print("\n" + "="*80)
        print("📊 REPORTE COMPLETO DE RESULTADOS")
        print("="*80)
        print()
        
        # Información general
        print("📈 INFORMACIÓN GENERAL")
        print("-"*80)
        print(f"Total de lugares extraídos: {len(self.df)}")
        print()
        
        # Por rubro
        if 'rubro_buscado' in self.df.columns:
            print("🏷️  DISTRIBUCIÓN POR RUBRO")
            print("-"*80)
            rubros = self.df['rubro_buscado'].value_counts()
            for rubro, count in rubros.items():
                porcentaje = (count / len(self.df)) * 100
                print(f"  {rubro:30} {count:5} lugares ({porcentaje:5.1f}%)")
            print()
        
        # Calidad de datos
        print("✨ CALIDAD DE DATOS")
        print("-"*80)
        
        campos = {
            'telefono': 'Teléfono',
            'sitio_web': 'Sitio web',
            'email': 'Email',
            'rating': 'Rating',
            'num_resenas': 'Número de reseñas',
            'latitud': 'Coordenadas'
        }
        
        for campo, nombre in campos.items():
            if campo in self.df.columns:
                con_dato = self.df[campo].notna().sum()
                porcentaje = (con_dato / len(self.df)) * 100
                print(f"  {nombre:20} {con_dato:5} ({porcentaje:5.1f}%)")
        
        print()
        
        # Estadísticas de ratings
        if 'rating' in self.df.columns:
            print("⭐ ESTADÍSTICAS DE RATINGS")
            print("-"*80)
            ratings = pd.to_numeric(self.df['rating'], errors='coerce').dropna()
            
            if len(ratings) > 0:
                print(f"  Rating promedio:     {ratings.mean():.2f}")
                print(f"  Rating mediano:      {ratings.median():.2f}")
                print(f"  Rating mínimo:       {ratings.min():.2f}")
                print(f"  Rating máximo:       {ratings.max():.2f}")
                print(f"  Desviación estándar: {ratings.std():.2f}")
                
                # Distribución de ratings
                print("\n  Distribución:")
                for i in range(5, 0, -1):
                    count = len(ratings[ratings >= i])
                    porcentaje = (count / len(ratings)) * 100
                    barra = "█" * int(porcentaje / 2)
                    print(f"    {i}+ estrellas: {barra} {porcentaje:5.1f}%")
            
            print()
        
        # Top lugares por reseñas
        if 'num_resenas' in self.df.columns and 'nombre' in self.df.columns:
            print("🔥 TOP 10 LUGARES MÁS POPULARES (por reseñas)")
            print("-"*80)
            
            df_resenas = self.df[self.df['num_resenas'].notna()].copy()
            df_resenas['num_resenas'] = pd.to_numeric(df_resenas['num_resenas'], errors='coerce')
            top_10 = df_resenas.nlargest(10, 'num_resenas')
            
            for idx, (_, row) in enumerate(top_10.iterrows(), 1):
                nombre = row['nombre'][:40]
                resenas = int(row['num_resenas']) if pd.notna(row['num_resenas']) else 0
                rating = row.get('rating', 'N/A')
                print(f"  {idx:2}. {nombre:40} - {resenas:6} reseñas (★{rating})")
            
            print()
        
        # Segmentación geográfica
        if 'segmento_id' in self.df.columns:
            print("🗺️  DISTRIBUCIÓN POR SEGMENTO GEOGRÁFICO")
            print("-"*80)
            segmentos = self.df['segmento_id'].value_counts()
            for segmento, count in segmentos.items():
                porcentaje = (count / len(self.df)) * 100
                print(f"  Segmento {segmento}: {count:5} lugares ({porcentaje:5.1f}%)")
            print()
        
        # Fechas de extracción
        if 'fecha_extraccion' in self.df.columns:
            print("📅 INFORMACIÓN TEMPORAL")
            print("-"*80)
            print(f"  Primera extracción: {self.df['fecha_extraccion'].min()}")
            print(f"  Última extracción:  {self.df['fecha_extraccion'].max()}")
            print()
        
        print("="*80)
    
    def exportar_por_rubro(self):
        """Exporta archivos separados por rubro"""
        if self.df is None or 'rubro_buscado' not in self.df.columns:
            print("No hay datos de rubros para exportar")
            return
        
        output_dir = Path('resultados/por_rubro')
        output_dir.mkdir(exist_ok=True)
        
        print("\n📁 Exportando por rubro...")
        
        rubros = self.df['rubro_buscado'].unique()
        
        for rubro in rubros:
            df_rubro = self.df[self.df['rubro_buscado'] == rubro]
            filename = f"{rubro.replace(' ', '_')}.xlsx"
            filepath = output_dir / filename
            
            df_rubro.to_excel(filepath, index=False, engine='openpyxl')
            print(f"  ✅ {rubro}: {len(df_rubro)} lugares -> {filepath}")
        
        print(f"\n✅ Exportados {len(rubros)} archivos")
    
    def generar_reporte_contactos(self):
        """Genera reporte de lugares con información de contacto completa"""
        if self.df is None:
            return
        
        print("\n📞 REPORTE DE CONTACTOS")
        print("="*80)
        
        # Lugares con teléfono Y sitio web
        if 'telefono' in self.df.columns and 'sitio_web' in self.df.columns:
            con_ambos = self.df[
                self.df['telefono'].notna() & 
                self.df['sitio_web'].notna()
            ]
            print(f"Con teléfono Y sitio web: {len(con_ambos)}")
            
            # Exportar
            if len(con_ambos) > 0:
                output_file = Path('resultados/contactos_completos.xlsx')
                con_ambos.to_excel(output_file, index=False, engine='openpyxl')
                print(f"  ✅ Exportado: {output_file}")
        
        # Lugares con teléfono pero sin sitio web
        if 'telefono' in self.df.columns and 'sitio_web' in self.df.columns:
            solo_telefono = self.df[
                self.df['telefono'].notna() & 
                self.df['sitio_web'].isna()
            ]
            print(f"Solo con teléfono: {len(solo_telefono)}")
        
        # Lugares sin información de contacto
        if 'telefono' in self.df.columns and 'sitio_web' in self.df.columns:
            sin_contacto = self.df[
                self.df['telefono'].isna() & 
                self.df['sitio_web'].isna()
            ]
            print(f"Sin información de contacto: {len(sin_contacto)}")
        
        print()
    
    def buscar_por_criterio(self, criterio):
        """Busca lugares que cumplan un criterio específico"""
        if self.df is None:
            return
        
        resultados = self.df
        
        # Aplicar filtros según criterio
        if criterio == 'top_rating':
            resultados = resultados[pd.to_numeric(resultados['rating'], errors='coerce') >= 4.5]
        elif criterio == 'muchas_resenas':
            resultados = resultados[pd.to_numeric(resultados['num_resenas'], errors='coerce') >= 100]
        elif criterio == 'con_web':
            resultados = resultados[resultados['sitio_web'].notna()]
        elif criterio == 'sin_web':
            resultados = resultados[resultados['sitio_web'].isna()]
        
        return resultados
    
    def generar_json_export(self):
        """Exporta datos en formato JSON"""
        if self.df is None:
            return
        
        output_file = Path('resultados/google_maps_results.json')
        
        # Convertir a formato JSON-friendly
        datos_json = self.df.to_dict('records')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Exportado a JSON: {output_file}")
        print(f"   {len(datos_json)} registros")


def main():
    """Función principal"""
    print("\n" + "="*80)
    print("📊 ANÁLISIS DE RESULTADOS - GOOGLE MAPS SCRAPER")
    print("="*80)
    
    analyzer = ResultadosAnalyzer()
    
    if not analyzer.cargar_datos():
        return 1
    
    # Generar reporte completo
    analyzer.generar_reporte_completo()
    
    # Reporte de contactos
    analyzer.generar_reporte_contactos()
    
    # Preguntar si quiere exportar por rubro
    print("\n" + "-"*80)
    respuesta = input("¿Deseas exportar archivos separados por rubro? (s/n): ").strip().lower()
    
    if respuesta == 's':
        analyzer.exportar_por_rubro()
    
    # Preguntar si quiere exportar JSON
    print("\n" + "-"*80)
    respuesta = input("¿Deseas exportar los datos en formato JSON? (s/n): ").strip().lower()
    
    if respuesta == 's':
        analyzer.generar_json_export()
    
    print("\n" + "="*80)
    print("✅ Análisis completado")
    print("="*80 + "\n")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
