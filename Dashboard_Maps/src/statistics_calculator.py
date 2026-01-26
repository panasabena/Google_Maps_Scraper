"""
Módulo para calcular estadísticas avanzadas del scraping.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timedelta
from collections import Counter


class StatisticsCalculator:
    """Clase para calcular estadísticas avanzadas."""
    
    def __init__(self, df: pd.DataFrame):
        """
        Inicializa el calculador de estadísticas.
        
        Args:
            df: DataFrame con los datos
        """
        self.df = df
    
    def get_overview_stats(self) -> Dict:
        """
        Obtiene estadísticas generales.
        
        Returns:
            Diccionario con estadísticas de resumen
        """
        if self.df is None or len(self.df) == 0:
            return self._empty_stats()
        
        total = len(self.df)
        
        stats = {
            # Totales
            'total_empresas': total,
            'total_provincias': int(self.df['provincia'].nunique()) if 'provincia' in self.df.columns else 0,
            'total_ciudades': int(self.df['ciudad'].nunique()) if 'ciudad' in self.df.columns else 0,
            'total_rubros': int(self.df['rubro_buscado'].nunique()) if 'rubro_buscado' in self.df.columns else 0,
            'total_categorias': int(self.df['categoria'].nunique()) if 'categoria' in self.df.columns else 0,
            
            # Calidad de datos
            'con_email': int(self.df['tiene_email'].sum()) if 'tiene_email' in self.df.columns else 0,
            'con_telefono': int(self.df['tiene_telefono'].sum()) if 'tiene_telefono' in self.df.columns else 0,
            'con_web': int(self.df['tiene_web'].sum()) if 'tiene_web' in self.df.columns else 0,
            'con_rating': int(self.df['tiene_rating'].sum()) if 'tiene_rating' in self.df.columns else 0,
            'con_coordenadas': int((self.df['latitud'].notna() & self.df['longitud'].notna()).sum()) if 'latitud' in self.df.columns else 0,
            
            # Ratings
            'rating_promedio': float(self.df['rating'].mean()) if 'rating' in self.df.columns else 0.0,
            'rating_mediano': float(self.df['rating'].median()) if 'rating' in self.df.columns else 0.0,
            'total_resenas': int(self.df['num_resenas'].sum()) if 'num_resenas' in self.df.columns else 0,
            'promedio_resenas': float(self.df['num_resenas'].mean()) if 'num_resenas' in self.df.columns else 0.0,
        }
        
        # Porcentajes
        if total > 0:
            stats['porcentaje_email'] = round((stats['con_email'] / total) * 100, 2)
            stats['porcentaje_telefono'] = round((stats['con_telefono'] / total) * 100, 2)
            stats['porcentaje_web'] = round((stats['con_web'] / total) * 100, 2)
            stats['porcentaje_rating'] = round((stats['con_rating'] / total) * 100, 2)
            stats['porcentaje_coordenadas'] = round((stats['con_coordenadas'] / total) * 100, 2)
            
            # Calidad general (promedio de completitud)
            completitud = (
                stats['porcentaje_email'] + 
                stats['porcentaje_telefono'] + 
                stats['porcentaje_web'] + 
                stats['porcentaje_rating']
            ) / 4
            stats['calidad_datos'] = round(completitud, 2)
        else:
            stats['porcentaje_email'] = 0
            stats['porcentaje_telefono'] = 0
            stats['porcentaje_web'] = 0
            stats['porcentaje_rating'] = 0
            stats['porcentaje_coordenadas'] = 0
            stats['calidad_datos'] = 0
        
        # Fechas
        if 'fecha_extraccion' in self.df.columns:
            stats['primera_extraccion'] = self.df['fecha_extraccion'].min()
            stats['ultima_extraccion'] = self.df['fecha_extraccion'].max()
            
            # Empresas extraídas hoy
            hoy = datetime.now().date()
            if pd.notna(stats['ultima_extraccion']):
                empresas_hoy = len(self.df[self.df['fecha_extraccion'].dt.date == hoy])
                stats['empresas_hoy'] = empresas_hoy
            else:
                stats['empresas_hoy'] = 0
        
        return stats
    
    def get_distribution_by_province(self) -> pd.DataFrame:
        """
        Obtiene distribución de empresas por provincia.
        
        Returns:
            DataFrame con estadísticas por provincia
        """
        if self.df is None or len(self.df) == 0 or 'provincia' not in self.df.columns:
            return pd.DataFrame()
        
        # Agrupar por provincia
        provincia_stats = self.df.groupby('provincia').agg({
            'nombre': 'count',
            'tiene_email': 'sum',
            'tiene_telefono': 'sum',
            'tiene_web': 'sum',
            'rating': 'mean',
            'num_resenas': 'sum'
        }).reset_index()
        
        provincia_stats.columns = [
            'provincia', 'total_empresas', 'con_email', 
            'con_telefono', 'con_web', 'rating_promedio', 'total_resenas'
        ]
        
        # Calcular porcentajes
        provincia_stats['porcentaje_email'] = round(
            (provincia_stats['con_email'] / provincia_stats['total_empresas']) * 100, 2
        )
        provincia_stats['porcentaje_telefono'] = round(
            (provincia_stats['con_telefono'] / provincia_stats['total_empresas']) * 100, 2
        )
        provincia_stats['porcentaje_web'] = round(
            (provincia_stats['con_web'] / provincia_stats['total_empresas']) * 100, 2
        )
        
        # Ordenar por total de empresas
        provincia_stats = provincia_stats.sort_values('total_empresas', ascending=False)
        
        return provincia_stats
    
    def get_distribution_by_category(self, top_n: int = 20) -> pd.DataFrame:
        """
        Obtiene distribución de empresas por categoría.
        
        Args:
            top_n: Número de categorías a devolver
            
        Returns:
            DataFrame con top categorías
        """
        if self.df is None or len(self.df) == 0 or 'categoria' not in self.df.columns:
            return pd.DataFrame()
        
        categoria_stats = self.df.groupby('categoria').agg({
            'nombre': 'count',
            'rating': 'mean',
            'tiene_email': 'sum',
            'tiene_telefono': 'sum'
        }).reset_index()
        
        categoria_stats.columns = [
            'categoria', 'total', 'rating_promedio', 'con_email', 'con_telefono'
        ]
        
        categoria_stats = categoria_stats.sort_values('total', ascending=False).head(top_n)
        
        return categoria_stats
    
    def get_distribution_by_rubro(self, top_n: int = 20) -> pd.DataFrame:
        """
        Obtiene distribución de empresas por rubro buscado.
        
        Args:
            top_n: Número de rubros a devolver
            
        Returns:
            DataFrame con top rubros
        """
        if self.df is None or len(self.df) == 0 or 'rubro_buscado' not in self.df.columns:
            return pd.DataFrame()
        
        rubro_stats = self.df.groupby('rubro_buscado').agg({
            'nombre': 'count',
            'rating': 'mean'
        }).reset_index()
        
        rubro_stats.columns = ['rubro', 'total', 'rating_promedio']
        rubro_stats = rubro_stats.sort_values('total', ascending=False).head(top_n)
        
        return rubro_stats
    
    def get_top_cities(self, top_n: int = 10) -> pd.DataFrame:
        """
        Obtiene las ciudades con más empresas.
        
        Args:
            top_n: Número de ciudades a devolver
            
        Returns:
            DataFrame con top ciudades
        """
        if self.df is None or len(self.df) == 0 or 'ciudad' not in self.df.columns:
            return pd.DataFrame()
        
        ciudad_stats = self.df['ciudad'].value_counts().head(top_n).reset_index()
        ciudad_stats.columns = ['ciudad', 'total_empresas']
        
        return ciudad_stats
    
    def get_timeline_data(self, periodo: str = 'dia') -> pd.DataFrame:
        """
        Obtiene datos de línea de tiempo de extracciones.
        
        Args:
            periodo: 'dia', 'semana' o 'mes'
            
        Returns:
            DataFrame con datos temporales
        """
        if self.df is None or len(self.df) == 0 or 'fecha_extraccion' not in self.df.columns:
            return pd.DataFrame()
        
        df_temp = self.df.copy()
        df_temp = df_temp[df_temp['fecha_extraccion'].notna()]
        
        if len(df_temp) == 0:
            return pd.DataFrame()
        
        # Agrupar por período
        if periodo == 'dia':
            df_temp['periodo'] = df_temp['fecha_extraccion'].dt.date
        elif periodo == 'semana':
            df_temp['periodo'] = df_temp['fecha_extraccion'].dt.to_period('W').apply(lambda x: x.start_time)
        elif periodo == 'mes':
            df_temp['periodo'] = df_temp['fecha_extraccion'].dt.to_period('M').apply(lambda x: x.start_time)
        else:
            df_temp['periodo'] = df_temp['fecha_extraccion'].dt.date
        
        timeline = df_temp.groupby('periodo').size().reset_index()
        timeline.columns = ['fecha', 'total_empresas']
        timeline = timeline.sort_values('fecha')
        
        # Calcular acumulado
        timeline['acumulado'] = timeline['total_empresas'].cumsum()
        
        return timeline
    
    def get_rating_distribution(self) -> Dict:
        """
        Obtiene distribución de ratings.
        
        Returns:
            Diccionario con distribución de ratings
        """
        if self.df is None or len(self.df) == 0 or 'rating' not in self.df.columns:
            return {}
        
        ratings = self.df[self.df['rating'].notna()]['rating']
        
        if len(ratings) == 0:
            return {}
        
        # Crear rangos de rating
        bins = [0, 1, 2, 3, 4, 5]
        labels = ['0-1', '1-2', '2-3', '3-4', '4-5']
        
        rating_counts = pd.cut(ratings, bins=bins, labels=labels, include_lowest=True).value_counts()
        
        distribution = {
            'rangos': labels,
            'conteos': rating_counts.reindex(labels, fill_value=0).tolist(),
            'total': len(ratings)
        }
        
        return distribution
    
    def get_quality_score_by_category(self, top_n: int = 10) -> pd.DataFrame:
        """
        Calcula score de calidad por categoría.
        
        Args:
            top_n: Número de categorías a devolver
            
        Returns:
            DataFrame con scores de calidad
        """
        if self.df is None or len(self.df) == 0:
            return pd.DataFrame()
        
        # Calcular score de calidad (0-100)
        df_temp = self.df.copy()
        df_temp['quality_score'] = (
            (df_temp['tiene_email'].astype(int) * 25) +
            (df_temp['tiene_telefono'].astype(int) * 25) +
            (df_temp['tiene_web'].astype(int) * 25) +
            (df_temp['tiene_rating'].astype(int) * 25)
        )
        
        # Agrupar por categoría
        quality_by_cat = df_temp.groupby('categoria').agg({
            'nombre': 'count',
            'quality_score': 'mean'
        }).reset_index()
        
        quality_by_cat.columns = ['categoria', 'total_empresas', 'quality_score']
        
        # Filtrar categorías con al menos 10 empresas
        quality_by_cat = quality_by_cat[quality_by_cat['total_empresas'] >= 10]
        
        # Ordenar por quality score
        quality_by_cat = quality_by_cat.sort_values('quality_score', ascending=False).head(top_n)
        
        return quality_by_cat
    
    def get_heatmap_data(self) -> List[List[float]]:
        """
        Obtiene datos para heatmap de empresas.
        
        Returns:
            Lista de [latitud, longitud, peso]
        """
        if self.df is None or len(self.df) == 0:
            return []
        
        # Filtrar empresas con coordenadas válidas
        df_coords = self.df[
            (self.df['latitud'].notna()) & 
            (self.df['longitud'].notna()) &
            (self.df['latitud'] != 0) & 
            (self.df['longitud'] != 0)
        ]
        
        if len(df_coords) == 0:
            return []
        
        # Crear lista de coordenadas
        heatmap_data = df_coords[['latitud', 'longitud']].values.tolist()
        
        # Agregar peso (1 por cada empresa, se puede ajustar)
        heatmap_data = [[lat, lng, 1] for lat, lng in heatmap_data]
        
        return heatmap_data
    
    def get_cluster_data(self) -> pd.DataFrame:
        """
        Obtiene datos para clustering de empresas.
        
        Returns:
            DataFrame con coordenadas y metadata para clusters
        """
        if self.df is None or len(self.df) == 0:
            return pd.DataFrame()
        
        # Filtrar empresas con coordenadas válidas
        df_coords = self.df[
            (self.df['latitud'].notna()) & 
            (self.df['longitud'].notna()) &
            (self.df['latitud'] != 0) & 
            (self.df['longitud'] != 0)
        ].copy()
        
        if len(df_coords) == 0:
            return pd.DataFrame()
        
        # Seleccionar columnas relevantes
        cols_relevantes = [
            'nombre', 'direccion', 'ciudad', 'provincia', 'categoria',
            'rating', 'num_resenas', 'telefono', 'sitio_web', 'email',
            'latitud', 'longitud', 'rubro_buscado'
        ]
        
        cols_disponibles = [col for col in cols_relevantes if col in df_coords.columns]
        
        return df_coords[cols_disponibles]
    
    def get_comparativa_provincial(self, provincias: List[str]) -> Dict:
        """
        Compara estadísticas entre provincias seleccionadas.
        
        Args:
            provincias: Lista de provincias a comparar
            
        Returns:
            Diccionario con comparativas
        """
        if self.df is None or len(self.df) == 0 or 'provincia' not in self.df.columns:
            return {}
        
        comparativa = {}
        
        for provincia in provincias:
            df_prov = self.df[self.df['provincia'] == provincia]
            
            if len(df_prov) == 0:
                continue
            
            comparativa[provincia] = {
                'total_empresas': len(df_prov),
                'con_email': int(df_prov['tiene_email'].sum()),
                'con_telefono': int(df_prov['tiene_telefono'].sum()),
                'con_web': int(df_prov['tiene_web'].sum()),
                'rating_promedio': float(df_prov['rating'].mean()) if 'rating' in df_prov.columns else 0,
                'total_rubros': int(df_prov['rubro_buscado'].nunique()) if 'rubro_buscado' in df_prov.columns else 0
            }
        
        return comparativa
    
    def _empty_stats(self) -> Dict:
        """Retorna estadísticas vacías."""
        return {
            'total_empresas': 0,
            'total_provincias': 0,
            'total_ciudades': 0,
            'total_rubros': 0,
            'total_categorias': 0,
            'con_email': 0,
            'con_telefono': 0,
            'con_web': 0,
            'con_rating': 0,
            'con_coordenadas': 0,
            'rating_promedio': 0.0,
            'rating_mediano': 0.0,
            'total_resenas': 0,
            'promedio_resenas': 0.0,
            'porcentaje_email': 0,
            'porcentaje_telefono': 0,
            'porcentaje_web': 0,
            'porcentaje_rating': 0,
            'porcentaje_coordenadas': 0,
            'calidad_datos': 0,
            'empresas_hoy': 0
        }
