"""
Módulo para generar mapas interactivos con Plotly y Dash Leaflet.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from typing import Dict, List, Tuple
import json


class MapGenerator:
    """Clase para generar mapas interactivos."""
    
    def __init__(self):
        """Inicializa el generador de mapas."""
        self.map_center = [-38.4161, -63.6167]  # Centro de Argentina
        self.map_zoom = 5
        
        # Colores para estados
        self.colors = {
            'completed': '#28a745',  # Verde
            'partial': '#ffc107',    # Amarillo
            'pending': '#dc3545',    # Rojo
            'default': '#6c757d'     # Gris
        }
    
    def create_ubicaciones_map(self, ubicaciones_status: List[Dict], df_empresas: pd.DataFrame = None) -> go.Figure:
        """
        Crea un mapa scatter con todas las empresas.
        
        Args:
            ubicaciones_status: Lista de diccionarios con estado de ubicaciones
            df_empresas: DataFrame con las empresas para mostrar como puntos
            
        Returns:
            Figura de Plotly con el mapa scatter
        """
        # Crear figura
        fig = go.Figure()
        
        print(f"\n{'='*60}")
        print(f"🗺️ GENERANDO MAPA DE EMPRESAS")
        print(f"{'='*60}")
        
        if df_empresas is None:
            print("❌ ERROR: No se recibió el DataFrame de empresas")
            return self._empty_map()
        
        print(f"📊 Total empresas recibidas: {len(df_empresas):,}")
        print(f"📋 Columnas disponibles: {list(df_empresas.columns)}")
        
        # Verificar que existan las columnas necesarias
        if 'latitud' not in df_empresas.columns or 'longitud' not in df_empresas.columns:
            print("❌ ERROR: No se encontraron columnas 'latitud' y 'longitud'")
            return self._empty_map()
        
        # Filtrar empresas con coordenadas válidas Y dentro de Argentina
        # Argentina: Latitud -55 a -21.8, Longitud -73.5 a -53.6
        df_coords = df_empresas[
            (df_empresas['latitud'].notna()) & 
            (df_empresas['longitud'].notna()) &
            (df_empresas['latitud'] != 0) & 
            (df_empresas['longitud'] != 0) &
            (df_empresas['latitud'] >= -55.5) &  # Sur de Argentina
            (df_empresas['latitud'] <= -21.5) &  # Norte de Argentina
            (df_empresas['longitud'] >= -74.0) &  # Oeste de Argentina
            (df_empresas['longitud'] <= -53.0)    # Este de Argentina
        ].copy()
        
        print(f"📍 Empresas con coordenadas válidas en Argentina: {len(df_coords):,}")
        
        if len(df_coords) == 0:
            print("❌ No hay empresas con coordenadas válidas en Argentina")
            return self._empty_map()
        
        # Mostrar estadísticas de coordenadas
        print(f"📐 Rango latitud: {df_coords['latitud'].min():.2f} a {df_coords['latitud'].max():.2f}")
        print(f"📐 Rango longitud: {df_coords['longitud'].min():.2f} a {df_coords['longitud'].max():.2f}")
        
        # Advertir si se filtraron muchas empresas
        coords_fuera = len(df_empresas) - len(df_coords)
        if coords_fuera > 100:
            print(f"⚠️  Se filtraron {coords_fuera:,} empresas con coordenadas fuera de Argentina")
        
        # Limitar a 3000 puntos para mejor rendimiento
        if len(df_coords) > 3000:
            df_coords = df_coords.sample(n=3000, random_state=42)
            print(f"🎲 Muestreadas a 3,000 empresas para rendimiento")
        
        # Crear texto hover simple
        df_coords['hover_text'] = df_coords.apply(
            lambda row: (
                f"<b>{str(row.get('nombre', 'N/A'))[:50]}</b><br>" +
                f"📍 {str(row.get('ciudad', 'N/A'))}<br>" +
                f"🏢 {str(row.get('categoria', 'N/A'))[:40]}<br>" +
                f"⭐ {row.get('rating', 'N/A')}"
            ),
            axis=1
        )
        
        # Agregar scatter con Scattermapbox (más eficiente)
        fig = go.Figure(go.Scattermapbox(
            lon=df_coords['longitud'],
            lat=df_coords['latitud'],
            mode='markers',
            marker=dict(
                size=8,
                color='#ffc107',
                opacity=0.6
            ),
            text=df_coords['hover_text'],
            hovertemplate='%{text}<extra></extra>',
            name=f'Empresas ({len(df_coords):,})'
        ))
        
        # Configurar el mapa con mapbox
        fig.update_layout(
            mapbox=dict(
                style='open-street-map',
                center=dict(lat=-38.4161, lon=-63.6167),
                zoom=4
            ),
            title={
                'text': f'Empresas Extraídas en Argentina ({len(df_coords):,} empresas)',
                'font': {'size': 18, 'color': '#2c3e50'},
                'x': 0.5,
                'xanchor': 'center'
            },
            height=700,
            margin=dict(l=0, r=0, t=60, b=0),
            showlegend=False
        )
        
        print(f"✅ Mapa generado exitosamente con {len(df_coords):,} puntos")
        print(f"{'='*60}\n")
        
        return fig
        
        # Configurar el layout del mapa geopolítico
        fig.update_geos(
            scope='south america',
            center=dict(lat=-38.4161, lon=-63.6167),
            projection_scale=6,
            projection_type='mercator',
            visible=True,
            resolution=50,
            showcountries=True,
            countrycolor='#2c3e50',
            countrywidth=2,
            showsubunits=True,  # Mostrar subdivisiones (provincias)
            subunitcolor='#95a5a6',
            subunitwidth=1,
            showland=True,
            landcolor='#ecf0f1',
            showlakes=True,
            lakecolor='#d4e9f7',
            showrivers=False,
            coastlinecolor='#34495e',
            coastlinewidth=1.5,
            bgcolor='#e8f4f8'
        )
        
        fig.update_layout(
            title={
                'text': 'Empresas Extraídas por Ubicación - Argentina',
                'font': {'size': 20, 'color': '#2c3e50', 'family': 'Arial'},
                'x': 0.5,
                'xanchor': 'center'
            },
            height=700,
            margin=dict(l=0, r=0, t=60, b=0),
            showlegend=True,
            legend=dict(
                orientation='v',
                yanchor='top',
                y=0.98,
                xanchor='left',
                x=0.02,
                bgcolor='rgba(255,255,255,0.95)',
                bordercolor='#cccccc',
                borderwidth=2,
                font=dict(size=13, family='Arial')
            ),
            paper_bgcolor='#ffffff',
            geo=dict(
                bgcolor='#e8f4f8'
            )
        )
        
        return fig
    
    def create_heatmap(self, df: pd.DataFrame) -> go.Figure:
        """
        Crea un mapa de densidad de empresas.
        
        Args:
            df: DataFrame con datos de empresas (debe tener latitud y longitud)
            
        Returns:
            Figura de Plotly con el heatmap
        """
        if df is None or len(df) == 0:
            return self._empty_map()
        
        # Filtrar empresas con coordenadas válidas
        df_coords = df[
            (df['latitud'].notna()) & 
            (df['longitud'].notna()) &
            (df['latitud'] != 0) & 
            (df['longitud'] != 0)
        ].copy()
        
        if len(df_coords) == 0:
            return self._empty_map()
        
        # Crear mapa de densidad
        fig = go.Figure(go.Densitymapbox(
            lat=df_coords['latitud'],
            lon=df_coords['longitud'],
            radius=10,
            colorscale='Viridis',
            showscale=True,
            hovertemplate='Densidad: %{z}<extra></extra>'
        ))
        
        fig.update_layout(
            mapbox_style='open-street-map',
            mapbox=dict(
                center=dict(lat=-38.4161, lon=-63.6167),
                zoom=4
            ),
            title='Densidad de Empresas Extraídas',
            height=600,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        return fig
    
    def create_scatter_map(self, df: pd.DataFrame, color_by: str = 'provincia') -> go.Figure:
        """
        Crea un mapa scatter de empresas coloreado por una categoría.
        
        Args:
            df: DataFrame con datos de empresas
            color_by: Columna por la cual colorear ('provincia', 'categoria', 'rubro_buscado')
            
        Returns:
            Figura de Plotly con el mapa scatter
        """
        if df is None or len(df) == 0:
            return self._empty_map()
        
        # Filtrar empresas con coordenadas válidas
        df_coords = df[
            (df['latitud'].notna()) & 
            (df['longitud'].notna()) &
            (df['latitud'] != 0) & 
            (df['longitud'] != 0)
        ].copy()
        
        if len(df_coords) == 0:
            return self._empty_map()
        
        # Limitar a una muestra si hay demasiados puntos (para rendimiento)
        if len(df_coords) > 10000:
            df_coords = df_coords.sample(n=10000, random_state=42)
        
        # Crear texto hover
        df_coords['hover_text'] = df_coords.apply(
            lambda row: f"<b>{row.get('nombre', 'N/A')}</b><br>" +
                       f"Categoría: {row.get('categoria', 'N/A')}<br>" +
                       f"Ciudad: {row.get('ciudad', 'N/A')}<br>" +
                       f"Rating: {row.get('rating', 'N/A')}",
            axis=1
        )
        
        # Crear el mapa
        if color_by in df_coords.columns:
            fig = px.scatter_mapbox(
                df_coords,
                lat='latitud',
                lon='longitud',
                color=color_by,
                hover_data=['nombre', 'categoria', 'ciudad', 'rating'],
                zoom=4,
                height=600,
                title=f'Empresas por {color_by.capitalize()}'
            )
        else:
            fig = px.scatter_mapbox(
                df_coords,
                lat='latitud',
                lon='longitud',
                hover_data=['nombre', 'categoria', 'ciudad', 'rating'],
                zoom=4,
                height=600,
                title='Empresas Extraídas'
            )
        
        fig.update_layout(
            mapbox_style='open-street-map',
            mapbox=dict(
                center=dict(lat=-38.4161, lon=-63.6167),
                zoom=4
            ),
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        return fig
    
    def create_choropleth_map(self, provincia_stats: pd.DataFrame, geojson_path: str = None) -> go.Figure:
        """
        Crea un mapa coroplético de provincias coloreado por número de empresas.
        
        Args:
            provincia_stats: DataFrame con estadísticas por provincia
            geojson_path: Ruta al archivo GeoJSON de provincias (opcional)
            
        Returns:
            Figura de Plotly con el mapa coroplético
        """
        if provincia_stats is None or len(provincia_stats) == 0:
            return self._empty_map()
        
        # Si tenemos el GeoJSON, crear mapa coroplético real
        if geojson_path:
            try:
                with open(geojson_path, 'r', encoding='utf-8') as f:
                    geojson_data = json.load(f)
                
                fig = go.Figure(go.Choroplethmapbox(
                    geojson=geojson_data,
                    locations=provincia_stats['provincia'],
                    z=provincia_stats['total_empresas'],
                    featureidkey='properties.nombre',  # Ajustar según estructura del GeoJSON
                    colorscale='Viridis',
                    text=provincia_stats['provincia'],
                    hovertemplate='<b>%{text}</b><br>Empresas: %{z}<extra></extra>',
                    marker_line_width=1,
                    marker_line_color='white'
                ))
                
                fig.update_layout(
                    mapbox_style='open-street-map',
                    mapbox=dict(
                        center=dict(lat=-38.4161, lon=-63.6167),
                        zoom=3.5
                    ),
                    title='Empresas por Provincia',
                    height=600,
                    margin=dict(l=0, r=0, t=40, b=0)
                )
                
                return fig
            except Exception as e:
                print(f"Error al cargar GeoJSON: {e}")
        
        # Si no hay GeoJSON o hubo error, crear un gráfico de barras
        fig = go.Figure(data=[
            go.Bar(
                x=provincia_stats['provincia'],
                y=provincia_stats['total_empresas'],
                marker_color='steelblue',
                hovertemplate='<b>%{x}</b><br>Empresas: %{y}<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Empresas por Provincia',
            xaxis_title='Provincia',
            yaxis_title='Total Empresas',
            height=500,
            xaxis={'categoryorder': 'total descending'},
            margin=dict(l=50, r=20, t=50, b=100)
        )
        
        fig.update_xaxes(tickangle=-45)
        
        return fig
    
    def create_progress_gauge(self, porcentaje: float, titulo: str = "Progreso General") -> go.Figure:
        """
        Crea un indicador de gauge para mostrar progreso.
        
        Args:
            porcentaje: Porcentaje de completado (0-100)
            titulo: Título del gauge
            
        Returns:
            Figura de Plotly con el gauge
        """
        # Determinar color según porcentaje
        if porcentaje >= 75:
            color = '#28a745'  # Verde
        elif porcentaje >= 50:
            color = '#ffc107'  # Amarillo
        elif porcentaje >= 25:
            color = '#fd7e14'  # Naranja
        else:
            color = '#dc3545'  # Rojo
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=porcentaje,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': titulo, 'font': {'size': 20}},
            delta={'reference': 100, 'increasing': {'color': color}},
            gauge={
                'axis': {'range': [None, 100], 'tickwidth': 1},
                'bar': {'color': color},
                'bgcolor': 'white',
                'borderwidth': 2,
                'bordercolor': 'gray',
                'steps': [
                    {'range': [0, 25], 'color': '#ffebee'},
                    {'range': [25, 50], 'color': '#fff3e0'},
                    {'range': [50, 75], 'color': '#fff9c4'},
                    {'range': [75, 100], 'color': '#e8f5e9'}
                ],
                'threshold': {
                    'line': {'color': 'red', 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_progress_donut(self, completado: int, pendiente: int) -> go.Figure:
        """
        Crea un gráfico de dona para mostrar progreso.
        
        Args:
            completado: Cantidad completada
            pendiente: Cantidad pendiente
            
        Returns:
            Figura de Plotly con el donut chart
        """
        labels = ['Completado', 'Pendiente']
        values = [completado, pendiente]
        colors = ['#28a745', '#e9ecef']
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            marker_colors=colors,
            textinfo='label+percent',
            textposition='outside',
            hovertemplate='<b>%{label}</b><br>%{value:,}<br>%{percent}<extra></extra>'
        )])
        
        # Agregar anotación en el centro
        total = completado + pendiente
        porcentaje = (completado / total * 100) if total > 0 else 0
        
        fig.add_annotation(
            text=f"{porcentaje:.1f}%",
            x=0.5, y=0.5,
            font_size=30,
            showarrow=False,
            font_color='#28a745' if porcentaje >= 50 else '#dc3545'
        )
        
        fig.update_layout(
            title='Progreso de Combinaciones',
            height=400,
            showlegend=True,
            margin=dict(l=20, r=20, t=60, b=20)
        )
        
        return fig
    
    def create_progress_bar_chart(self, provincias_progress: List[Dict]) -> go.Figure:
        """
        Crea un gráfico de barras horizontales con progreso por provincia.
        
        Args:
            provincias_progress: Lista con progreso por provincia
            
        Returns:
            Figura de Plotly con barras
        """
        if not provincias_progress:
            return go.Figure()
        
        df_progress = pd.DataFrame(provincias_progress)
        df_progress = df_progress.sort_values('porcentaje_completado', ascending=True)
        
        # Crear barras coloreadas por porcentaje
        colors_bar = df_progress['porcentaje_completado'].apply(
            lambda x: '#28a745' if x >= 75 else '#ffc107' if x >= 50 else '#fd7e14' if x >= 25 else '#dc3545'
        )
        
        fig = go.Figure(data=[
            go.Bar(
                x=df_progress['porcentaje_completado'],
                y=df_progress['provincia'],
                orientation='h',
                marker_color=colors_bar,
                text=df_progress['porcentaje_completado'].apply(lambda x: f"{x:.1f}%"),
                textposition='outside',
                hovertemplate='<b>%{y}</b><br>Completado: %{x:.1f}%<extra></extra>'
            )
        ])
        
        fig.update_layout(
            title='Progreso por Provincia',
            xaxis_title='Porcentaje Completado',
            yaxis_title='',
            height=max(400, len(provincias_progress) * 25),
            xaxis=dict(range=[0, 105]),
            margin=dict(l=150, r=50, t=50, b=50)
        )
        
        return fig
    
    def _empty_map(self) -> go.Figure:
        """Retorna un mapa vacío."""
        fig = go.Figure()
        
        fig.update_geos(
            scope='south america',
            center=dict(lat=-38.4161, lon=-63.6167),
            projection_scale=4,
            showcountries=True,
            countrycolor='lightgray'
        )
        
        fig.update_layout(
            title='Sin datos disponibles',
            height=600,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        return fig
