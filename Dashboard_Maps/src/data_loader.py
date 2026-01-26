"""
Módulo para cargar y procesar datos del scraping de Google Maps.
"""

import pandas as pd
import json
import os
from typing import Dict, List, Tuple
from datetime import datetime
import numpy as np


class DataLoader:
    """Clase para cargar y procesar datos del scraping."""
    
    def __init__(self, csv_path: str, json_path: str, config_path: str = None):
        """
        Inicializa el cargador de datos.
        
        Args:
            csv_path: Ruta al archivo CSV con los resultados
            json_path: Ruta al archivo JSON con el estado de ejecución
            config_path: Ruta al archivo config.py (opcional)
        """
        self.csv_path = csv_path
        self.json_path = json_path
        self.config_path = config_path
        
        self.df = None
        self.estado = None
        self.config = None
        
        # Cache
        self._last_modified_csv = None
        self._last_modified_json = None
    
    def cargar_datos(self, force_reload: bool = False) -> pd.DataFrame:
        """
        Carga los datos del CSV.
        
        Args:
            force_reload: Si es True, fuerza la recarga aunque no haya cambios
            
        Returns:
            DataFrame con los datos
        """
        try:
            # Verificar si el archivo ha cambiado
            current_modified = os.path.getmtime(self.csv_path)
            
            if force_reload or self.df is None or self._last_modified_csv != current_modified:
                print(f"📂 Cargando datos desde {self.csv_path}...")
                
                # Cargar CSV con tipos optimizados
                dtype_dict = {
                    'nombre': 'str',
                    'direccion': 'str',
                    'ciudad': 'str',
                    'categoria': 'str',
                    'telefono': 'str',
                    'sitio_web': 'str',
                    'email': 'str',
                    'url_google_maps': 'str',
                    'rubro_buscado': 'str',
                    'segmento_centro': 'str',
                }
                
                # Cargar en chunks si el archivo es muy grande
                file_size = os.path.getsize(self.csv_path) / (1024 * 1024)  # MB
                
                if file_size > 100:  # Si es mayor a 100MB
                    chunks = []
                    chunk_size = 10000
                    
                    for chunk in pd.read_csv(self.csv_path, dtype=dtype_dict, chunksize=chunk_size):
                        chunks.append(chunk)
                    
                    self.df = pd.concat(chunks, ignore_index=True)
                else:
                    self.df = pd.read_csv(self.csv_path, dtype=dtype_dict)
                
                # Procesar datos
                self._procesar_datos()
                
                self._last_modified_csv = current_modified
                print(f"✅ Datos cargados: {len(self.df):,} registros")
            else:
                print("ℹ️ Usando datos en caché (sin cambios en el archivo)")
            
            return self.df
            
        except Exception as e:
            print(f"❌ Error al cargar datos: {e}")
            return pd.DataFrame()
    
    def _procesar_datos(self):
        """Procesa y limpia los datos cargados."""
        if self.df is None or len(self.df) == 0:
            return
        
        # Convertir fechas
        if 'fecha_extraccion' in self.df.columns:
            self.df['fecha_extraccion'] = pd.to_datetime(
                self.df['fecha_extraccion'], 
                errors='coerce'
            )
        
        # Extraer coordenadas individuales de cada negocio desde las URLs de Google Maps
        # Formato URL: !3d-34.6158871!4d-58.5273434
        print(f"   🔍 Extrayendo coordenadas individuales desde URLs de Google Maps...")
        
        if 'url_google_maps' in self.df.columns:
            print(f"   📝 Muestra URL: {self.df['url_google_maps'].iloc[0][:100] if len(self.df) > 0 else 'N/A'}...")
            
            def extraer_coords_url(url):
                """Extrae lat/lng de URLs tipo: !3d-34.6158871!4d-58.5273434"""
                if pd.isna(url):
                    return None, None
                url_str = str(url)
                
                try:
                    import re
                    # Buscar el PRIMER !3d (latitud) y !4d (longitud)
                    lat_match = re.search(r'!3d(-?\d+\.?\d*)', url_str)
                    lng_match = re.search(r'!4d(-?\d+\.?\d*)', url_str)
                    
                    if lat_match and lng_match:
                        lat = float(lat_match.group(1))
                        lng = float(lng_match.group(1))
                        return lat, lng
                except Exception as e:
                    pass
                return None, None
            
            # Aplicar extracción
            coords = self.df['url_google_maps'].apply(extraer_coords_url)
            self.df['latitud'] = coords.apply(lambda x: x[0])
            self.df['longitud'] = coords.apply(lambda x: x[1])
            
            print(f"   ✅ Latitudes extraídas: {self.df['latitud'].notna().sum():,} de {len(self.df):,}")
            print(f"   ✅ Longitudes extraídas: {self.df['longitud'].notna().sum():,} de {len(self.df):,}")
            
            # Mostrar rango para verificar que están en Argentina
            if self.df['latitud'].notna().any():
                print(f"   📐 Rango latitud: {self.df['latitud'].min():.2f} a {self.df['latitud'].max():.2f}")
                print(f"   📐 Rango longitud: {self.df['longitud'].min():.2f} a {self.df['longitud'].max():.2f}")
        else:
            print(f"   ⚠️  Columna 'url_google_maps' NO encontrada")
            print(f"   📋 Columnas disponibles: {list(self.df.columns)}")
        
        # Limpiar y convertir rating
        if 'rating' in self.df.columns:
            self.df['rating'] = pd.to_numeric(self.df['rating'], errors='coerce')
        
        # Convertir número de reseñas
        if 'num_resenas' in self.df.columns:
            self.df['num_resenas'] = pd.to_numeric(self.df['num_resenas'], errors='coerce')
        
        # Crear columnas de flags para facilitar filtros
        self.df['tiene_email'] = self.df['email'].notna() & (self.df['email'] != '')
        self.df['tiene_telefono'] = self.df['telefono'].notna() & (self.df['telefono'] != '')
        self.df['tiene_web'] = self.df['sitio_web'].notna() & (self.df['sitio_web'] != '')
        self.df['tiene_rating'] = self.df['rating'].notna()
        
        # Extraer provincia de ciudad (simplificado)
        if 'ciudad' in self.df.columns:
            self.df['provincia'] = self.df['ciudad'].apply(self._extraer_provincia)
        
        # Remover duplicados (por URL de Google Maps)
        if 'url_google_maps' in self.df.columns:
            before = len(self.df)
            self.df = self.df.drop_duplicates(subset=['url_google_maps'], keep='first')
            after = len(self.df)
            if before != after:
                print(f"ℹ️ Duplicados removidos: {before - after}")
    
    def _extraer_provincia(self, ciudad: str) -> str:
        """
        Extrae la provincia de la ciudad.
        
        Args:
            ciudad: Nombre de la ciudad (ej: "Buenos Aires, Argentina")
            
        Returns:
            Nombre de la provincia
        """
        if pd.isna(ciudad):
            return "Desconocido"
        
        # Mapeo de ciudades principales a provincias
        mapeo = {
            'Buenos Aires': 'Buenos Aires',
            'Córdoba': 'Córdoba',
            'Rosario': 'Santa Fe',
            'Mendoza': 'Mendoza',
            'Tucumán': 'Tucumán',
            'La Plata': 'Buenos Aires',
            'Mar del Plata': 'Buenos Aires',
            'Salta': 'Salta',
            'Santa Fe': 'Santa Fe',
            'Resistencia': 'Chaco',
            'Santiago del Estero': 'Santiago del Estero',
            'Corrientes': 'Corrientes',
            'Neuquén': 'Neuquén',
            'Bahía Blanca': 'Buenos Aires',
            'San Salvador de Jujuy': 'Jujuy',
            'Posadas': 'Misiones',
            'Paraná': 'Entre Ríos',
            'San Luis': 'San Luis',
            'Río Gallegos': 'Santa Cruz',
            'Comodoro Rivadavia': 'Chubut',
            'Ushuaia': 'Tierra del Fuego',
            'Formosa': 'Formosa',
            'Quilmes': 'Buenos Aires',
            'Morón': 'Buenos Aires',
            'San Martín': 'Buenos Aires',
            'Lanús': 'Buenos Aires',
            'Lomas de Zamora': 'Buenos Aires',
            'Tigre': 'Buenos Aires',
            'Pilar': 'Buenos Aires',
        }
        
        # Buscar en el mapeo
        for ciudad_key, provincia in mapeo.items():
            if ciudad_key.lower() in ciudad.lower():
                return provincia
        
        # Si no se encuentra, devolver la primera parte antes de la coma
        partes = ciudad.split(',')
        if len(partes) > 0:
            return partes[0].strip()
        
        return "Desconocido"
    
    def cargar_estado(self, force_reload: bool = False) -> Dict:
        """
        Carga el estado de ejecución desde el JSON.
        
        Args:
            force_reload: Si es True, fuerza la recarga
            
        Returns:
            Diccionario con el estado
        """
        try:
            current_modified = os.path.getmtime(self.json_path)
            
            if force_reload or self.estado is None or self._last_modified_json != current_modified:
                print(f"📂 Cargando estado desde {self.json_path}...")
                
                with open(self.json_path, 'r', encoding='utf-8') as f:
                    self.estado = json.load(f)
                
                self._last_modified_json = current_modified
                print("✅ Estado cargado correctamente")
            else:
                print("ℹ️ Usando estado en caché")
            
            return self.estado
            
        except Exception as e:
            print(f"❌ Error al cargar estado: {e}")
            return {}
    
    def cargar_config(self) -> Dict:
        """
        Carga la configuración desde config.py.
        
        Returns:
            Diccionario con la configuración
        """
        if self.config is not None:
            return self.config
        
        try:
            if self.config_path and os.path.exists(self.config_path):
                # Importar el módulo config
                import importlib.util
                spec = importlib.util.spec_from_file_location("config", self.config_path)
                config_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(config_module)
                
                self.config = config_module.CONFIG
                print("✅ Configuración cargada")
            else:
                # Config por defecto si no existe el archivo
                self.config = {
                    'ubicaciones': [],
                    'rubros': []
                }
                print("⚠️ Usando configuración por defecto")
            
            return self.config
            
        except Exception as e:
            print(f"❌ Error al cargar configuración: {e}")
            return {'ubicaciones': [], 'rubros': []}
    
    def obtener_estadisticas_basicas(self) -> Dict:
        """
        Calcula estadísticas básicas de los datos.
        
        Returns:
            Diccionario con estadísticas
        """
        if self.df is None or len(self.df) == 0:
            return {}
        
        stats = {
            'total_empresas': len(self.df),
            'con_email': int(self.df['tiene_email'].sum()),
            'con_telefono': int(self.df['tiene_telefono'].sum()),
            'con_web': int(self.df['tiene_web'].sum()),
            'con_rating': int(self.df['tiene_rating'].sum()),
            'rating_promedio': float(self.df['rating'].mean()) if 'rating' in self.df.columns else 0,
            'total_provincias': int(self.df['provincia'].nunique()) if 'provincia' in self.df.columns else 0,
            'total_rubros': int(self.df['rubro_buscado'].nunique()) if 'rubro_buscado' in self.df.columns else 0,
        }
        
        # Porcentajes
        if stats['total_empresas'] > 0:
            stats['porcentaje_email'] = round((stats['con_email'] / stats['total_empresas']) * 100, 2)
            stats['porcentaje_telefono'] = round((stats['con_telefono'] / stats['total_empresas']) * 100, 2)
            stats['porcentaje_web'] = round((stats['con_web'] / stats['total_empresas']) * 100, 2)
        
        return stats
    
    def filtrar_datos(self, 
                     provincias: List[str] = None,
                     rubros: List[str] = None,
                     fecha_desde: datetime = None,
                     fecha_hasta: datetime = None,
                     tiene_email: bool = None,
                     tiene_telefono: bool = None,
                     tiene_web: bool = None,
                     min_rating: float = None,
                     max_rating: float = None) -> pd.DataFrame:
        """
        Filtra los datos según los criterios especificados.
        
        Args:
            provincias: Lista de provincias a incluir
            rubros: Lista de rubros a incluir
            fecha_desde: Fecha mínima de extracción
            fecha_hasta: Fecha máxima de extracción
            tiene_email: Si True, solo empresas con email
            tiene_telefono: Si True, solo empresas con teléfono
            tiene_web: Si True, solo empresas con sitio web
            min_rating: Rating mínimo
            max_rating: Rating máximo
            
        Returns:
            DataFrame filtrado
        """
        if self.df is None or len(self.df) == 0:
            return pd.DataFrame()
        
        df_filtrado = self.df.copy()
        
        # Filtrar por provincia
        if provincias and len(provincias) > 0:
            df_filtrado = df_filtrado[df_filtrado['provincia'].isin(provincias)]
        
        # Filtrar por rubro
        if rubros and len(rubros) > 0:
            df_filtrado = df_filtrado[df_filtrado['rubro_buscado'].isin(rubros)]
        
        # Filtrar por fechas
        if fecha_desde and 'fecha_extraccion' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['fecha_extraccion'] >= fecha_desde]
        
        if fecha_hasta and 'fecha_extraccion' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['fecha_extraccion'] <= fecha_hasta]
        
        # Filtrar por presencia de datos
        if tiene_email is True:
            df_filtrado = df_filtrado[df_filtrado['tiene_email'] == True]
        
        if tiene_telefono is True:
            df_filtrado = df_filtrado[df_filtrado['tiene_telefono'] == True]
        
        if tiene_web is True:
            df_filtrado = df_filtrado[df_filtrado['tiene_web'] == True]
        
        # Filtrar por rating
        if min_rating is not None and 'rating' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['rating'] >= min_rating]
        
        if max_rating is not None and 'rating' in df_filtrado.columns:
            df_filtrado = df_filtrado[df_filtrado['rating'] <= max_rating]
        
        return df_filtrado
    
    def obtener_top_n(self, columna: str, n: int = 10, filtro_df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Obtiene el top N de una columna.
        
        Args:
            columna: Nombre de la columna
            n: Número de elementos a devolver
            filtro_df: DataFrame filtrado (si es None, usa self.df)
            
        Returns:
            DataFrame con el top N
        """
        df = filtro_df if filtro_df is not None else self.df
        
        if df is None or len(df) == 0 or columna not in df.columns:
            return pd.DataFrame()
        
        return df[columna].value_counts().head(n).reset_index()
    
    def necesita_actualizacion(self) -> Tuple[bool, bool]:
        """
        Verifica si los archivos han cambiado y necesitan actualización.
        
        Returns:
            Tupla (csv_cambio, json_cambio)
        """
        csv_cambio = False
        json_cambio = False
        
        try:
            if self._last_modified_csv:
                current_csv = os.path.getmtime(self.csv_path)
                csv_cambio = current_csv != self._last_modified_csv
            
            if self._last_modified_json:
                current_json = os.path.getmtime(self.json_path)
                json_cambio = current_json != self._last_modified_json
        except Exception as e:
            print(f"⚠️ Error al verificar cambios: {e}")
        
        return csv_cambio, json_cambio
