"""
Módulo para rastrear el progreso del scraping de Google Maps.
"""

import json
from typing import Dict, List, Tuple
from datetime import datetime
import sys
import os

# Agregar el path del directorio raíz para importar config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import UBICACIONES_ARGENTINA, RUBROS_BUSQUEDA, get_total_combinaciones
except ImportError:
    # Fallback si no se puede importar config
    UBICACIONES_ARGENTINA = {}
    RUBROS_BUSQUEDA = []
    def get_total_combinaciones():
        return 0


class ProgressTracker:
    """Clase para rastrear el progreso del scraping."""
    
    def __init__(self, estado: Dict):
        """
        Inicializa el tracker de progreso.
        
        Args:
            estado: Diccionario con el estado de ejecución desde JSON
        """
        self.estado = estado if estado else {}
        self.ubicaciones_config = UBICACIONES_ARGENTINA
        self.rubros_config = RUBROS_BUSQUEDA
        self.total_combinaciones = get_total_combinaciones()
    
    def get_progress_summary(self) -> Dict:
        """
        Obtiene un resumen del progreso general.
        
        Returns:
            Diccionario con estadísticas de progreso
        """
        if not self.estado or 'ubicaciones_completadas' not in self.estado:
            return self._empty_progress()
        
        ubicaciones_completadas = self.estado.get('ubicaciones_completadas', {})
        
        # Contar combinaciones completadas
        combinaciones_completadas = 0
        ubicaciones_totales = len(self.ubicaciones_config)
        ubicaciones_100_pct = 0
        ubicaciones_parciales = 0
        ubicaciones_sin_procesar = 0
        
        total_rubros = len(self.rubros_config)
        
        for ubicacion_key, ubicacion_data in self.ubicaciones_config.items():
            if ubicacion_key in ubicaciones_completadas:
                rubros_completados = ubicaciones_completadas[ubicacion_key].get('rubros_completados', [])
                num_rubros = len(rubros_completados)
                combinaciones_completadas += num_rubros
                
                if num_rubros == total_rubros:
                    ubicaciones_100_pct += 1
                elif num_rubros > 0:
                    ubicaciones_parciales += 1
                else:
                    ubicaciones_sin_procesar += 1
            else:
                ubicaciones_sin_procesar += 1
        
        # Calcular porcentajes
        porcentaje_completado = 0
        if self.total_combinaciones > 0:
            porcentaje_completado = round((combinaciones_completadas / self.total_combinaciones) * 100, 2)
        
        return {
            'total_combinaciones': self.total_combinaciones,
            'combinaciones_completadas': combinaciones_completadas,
            'combinaciones_pendientes': self.total_combinaciones - combinaciones_completadas,
            'porcentaje_completado': porcentaje_completado,
            'porcentaje_pendiente': round(100 - porcentaje_completado, 2),
            
            'total_ubicaciones': ubicaciones_totales,
            'ubicaciones_completas': ubicaciones_100_pct,
            'ubicaciones_parciales': ubicaciones_parciales,
            'ubicaciones_sin_procesar': ubicaciones_sin_procesar,
            
            'total_rubros': total_rubros,
            
            # Porcentajes de ubicaciones
            'porcentaje_ubicaciones_completas': round((ubicaciones_100_pct / ubicaciones_totales) * 100, 2) if ubicaciones_totales > 0 else 0,
            'porcentaje_ubicaciones_parciales': round((ubicaciones_parciales / ubicaciones_totales) * 100, 2) if ubicaciones_totales > 0 else 0,
            'porcentaje_ubicaciones_sin_procesar': round((ubicaciones_sin_procesar / ubicaciones_totales) * 100, 2) if ubicaciones_totales > 0 else 0,
        }
    
    def get_ubicaciones_status(self) -> List[Dict]:
        """
        Obtiene el estado de cada ubicación.
        
        Returns:
            Lista de diccionarios con información de cada ubicación
        """
        ubicaciones_status = []
        ubicaciones_completadas = self.estado.get('ubicaciones_completadas', {})
        total_rubros = len(self.rubros_config)
        
        for ubicacion_key, ubicacion_data in self.ubicaciones_config.items():
            status_info = {
                'ubicacion_key': ubicacion_key,
                'nombre': ubicacion_data.get('nombre', ubicacion_key),
                'provincia': ubicacion_data.get('provincia', 'Desconocido'),
                'lat': ubicacion_data.get('lat', 0),
                'lng': ubicacion_data.get('lng', 0),
                'rubros_completados': 0,
                'total_rubros': total_rubros,
                'porcentaje_completado': 0,
                'estado': 'pending',  # 'completed', 'partial', 'pending'
                'ultima_actualizacion': None,
                'rubros_lista': []
            }
            
            if ubicacion_key in ubicaciones_completadas:
                rubros_completados = ubicaciones_completadas[ubicacion_key].get('rubros_completados', [])
                
                # Contar solo los rubros que están en la lista actual de config
                rubros_validos = [r for r in rubros_completados if r in self.rubros_config]
                
                status_info['rubros_completados'] = len(rubros_validos)
                status_info['rubros_lista'] = rubros_validos
                
                if total_rubros > 0:
                    status_info['porcentaje_completado'] = round((len(rubros_validos) / total_rubros) * 100, 2)
                
                # Determinar estado
                if len(rubros_validos) >= total_rubros:
                    status_info['estado'] = 'completed'
                elif len(rubros_validos) > 0:
                    status_info['estado'] = 'partial'
                else:
                    status_info['estado'] = 'pending'
                
                # Última actualización (si está disponible)
                if 'ultima_actualizacion' in ubicaciones_completadas[ubicacion_key]:
                    status_info['ultima_actualizacion'] = ubicaciones_completadas[ubicacion_key]['ultima_actualizacion']
            
            ubicaciones_status.append(status_info)
        
        return ubicaciones_status
    
    def get_provincias_progress(self) -> List[Dict]:
        """
        Obtiene el progreso agrupado por provincia.
        
        Returns:
            Lista de diccionarios con progreso por provincia
        """
        provincias_dict = {}
        ubicaciones_status = self.get_ubicaciones_status()
        total_rubros = len(self.rubros_config)
        
        for ubicacion in ubicaciones_status:
            provincia = ubicacion['provincia']
            
            if provincia not in provincias_dict:
                provincias_dict[provincia] = {
                    'provincia': provincia,
                    'ubicaciones': [],
                    'total_ubicaciones': 0,
                    'rubros_completados': 0,
                    'total_rubros_posibles': 0,
                    'ubicaciones_completas': 0,
                    'ubicaciones_parciales': 0,
                    'ubicaciones_sin_procesar': 0
                }
            
            provincias_dict[provincia]['ubicaciones'].append(ubicacion['nombre'])
            provincias_dict[provincia]['total_ubicaciones'] += 1
            provincias_dict[provincia]['rubros_completados'] += ubicacion['rubros_completados']
            provincias_dict[provincia]['total_rubros_posibles'] += total_rubros
            
            if ubicacion['estado'] == 'completed':
                provincias_dict[provincia]['ubicaciones_completas'] += 1
            elif ubicacion['estado'] == 'partial':
                provincias_dict[provincia]['ubicaciones_parciales'] += 1
            else:
                provincias_dict[provincia]['ubicaciones_sin_procesar'] += 1
        
        # Calcular porcentajes
        for provincia_data in provincias_dict.values():
            if provincia_data['total_rubros_posibles'] > 0:
                provincia_data['porcentaje_completado'] = round(
                    (provincia_data['rubros_completados'] / provincia_data['total_rubros_posibles']) * 100, 2
                )
            else:
                provincia_data['porcentaje_completado'] = 0
        
        # Convertir a lista y ordenar por porcentaje
        provincias_list = list(provincias_dict.values())
        provincias_list.sort(key=lambda x: x['porcentaje_completado'], reverse=True)
        
        return provincias_list
    
    def get_rubros_progress(self) -> List[Dict]:
        """
        Obtiene el progreso de cada rubro a través de todas las ubicaciones.
        
        Returns:
            Lista de diccionarios con progreso por rubro
        """
        rubros_progress = []
        ubicaciones_completadas = self.estado.get('ubicaciones_completadas', {})
        total_ubicaciones = len(self.ubicaciones_config)
        
        for rubro in self.rubros_config:
            ubicaciones_con_rubro = 0
            
            for ubicacion_key in self.ubicaciones_config.keys():
                if ubicacion_key in ubicaciones_completadas:
                    rubros_completados = ubicaciones_completadas[ubicacion_key].get('rubros_completados', [])
                    if rubro in rubros_completados:
                        ubicaciones_con_rubro += 1
            
            porcentaje = 0
            if total_ubicaciones > 0:
                porcentaje = round((ubicaciones_con_rubro / total_ubicaciones) * 100, 2)
            
            rubros_progress.append({
                'rubro': rubro,
                'ubicaciones_completadas': ubicaciones_con_rubro,
                'total_ubicaciones': total_ubicaciones,
                'porcentaje_completado': porcentaje
            })
        
        # Ordenar por porcentaje completado
        rubros_progress.sort(key=lambda x: x['porcentaje_completado'], reverse=True)
        
        return rubros_progress
    
    def get_ubicaciones_pendientes(self, limit: int = None) -> List[Dict]:
        """
        Obtiene las ubicaciones que aún tienen rubros pendientes.
        
        Args:
            limit: Número máximo de ubicaciones a retornar
            
        Returns:
            Lista de ubicaciones pendientes
        """
        ubicaciones_status = self.get_ubicaciones_status()
        
        # Filtrar ubicaciones no completadas
        pendientes = [
            ubicacion for ubicacion in ubicaciones_status 
            if ubicacion['estado'] != 'completed'
        ]
        
        # Ordenar por porcentaje completado (priorizar las que están más avanzadas)
        pendientes.sort(key=lambda x: x['porcentaje_completado'], reverse=True)
        
        if limit:
            pendientes = pendientes[:limit]
        
        return pendientes
    
    def get_rubros_pendientes_por_ubicacion(self, ubicacion_key: str) -> List[str]:
        """
        Obtiene los rubros pendientes para una ubicación específica.
        
        Args:
            ubicacion_key: Clave de la ubicación
            
        Returns:
            Lista de rubros pendientes
        """
        ubicaciones_completadas = self.estado.get('ubicaciones_completadas', {})
        
        if ubicacion_key not in ubicaciones_completadas:
            # Si no está en el estado, todos los rubros están pendientes
            return self.rubros_config.copy()
        
        rubros_completados = ubicaciones_completadas[ubicacion_key].get('rubros_completados', [])
        rubros_pendientes = [rubro for rubro in self.rubros_config if rubro not in rubros_completados]
        
        return rubros_pendientes
    
    def estimate_time_to_completion(self, empresas_por_dia: float = None, df=None) -> Dict:
        """
        Estima el tiempo para completar el scraping.
        
        Args:
            empresas_por_dia: Promedio de empresas extraídas por día (opcional)
            df: DataFrame con datos para calcular velocidad histórica
            
        Returns:
            Diccionario con estimaciones
        """
        progress = self.get_progress_summary()
        combinaciones_pendientes = progress['combinaciones_pendientes']
        
        # Si no hay combinaciones pendientes, ya terminamos
        if combinaciones_pendientes == 0:
            return {
                'completado': True,
                'dias_restantes': 0,
                'fecha_estimada': datetime.now().strftime('%Y-%m-%d')
            }
        
        # Calcular velocidad histórica si tenemos el DataFrame
        if df is not None and 'fecha_extraccion' in df.columns:
            df_temp = df[df['fecha_extraccion'].notna()].copy()
            
            if len(df_temp) > 0:
                # Calcular días únicos de extracción
                fechas_unicas = df_temp['fecha_extraccion'].dt.date.unique()
                num_dias = len(fechas_unicas)
                
                if num_dias > 0:
                    empresas_por_dia = len(df_temp) / num_dias
        
        # Si no tenemos velocidad, asumir un valor por defecto
        if empresas_por_dia is None or empresas_por_dia == 0:
            empresas_por_dia = 100  # Valor por defecto conservador
        
        # Estimar empresas promedio por combinación (muy variable, estimación)
        empresas_por_combinacion = 50  # Estimación conservadora
        
        # Calcular días restantes
        dias_restantes = (combinaciones_pendientes * empresas_por_combinacion) / empresas_por_dia
        dias_restantes = int(dias_restantes) + 1
        
        # Fecha estimada de completado
        from datetime import timedelta
        fecha_estimada = datetime.now() + timedelta(days=dias_restantes)
        
        return {
            'completado': False,
            'dias_restantes': dias_restantes,
            'fecha_estimada': fecha_estimada.strftime('%Y-%m-%d'),
            'empresas_por_dia': round(empresas_por_dia, 2),
            'combinaciones_pendientes': combinaciones_pendientes
        }
    
    def get_marker_data_for_map(self) -> List[Dict]:
        """
        Obtiene datos formateados para marcadores en el mapa.
        
        Returns:
            Lista de diccionarios con datos para marcadores
        """
        ubicaciones_status = self.get_ubicaciones_status()
        markers = []
        
        for ubicacion in ubicaciones_status:
            marker = {
                'lat': ubicacion['lat'],
                'lng': ubicacion['lng'],
                'nombre': ubicacion['nombre'],
                'provincia': ubicacion['provincia'],
                'estado': ubicacion['estado'],
                'porcentaje': ubicacion['porcentaje_completado'],
                'rubros_completados': ubicacion['rubros_completados'],
                'total_rubros': ubicacion['total_rubros'],
                'popup_html': self._generate_popup_html(ubicacion)
            }
            markers.append(marker)
        
        return markers
    
    def _generate_popup_html(self, ubicacion: Dict) -> str:
        """
        Genera HTML para el popup de un marcador.
        
        Args:
            ubicacion: Diccionario con información de la ubicación
            
        Returns:
            String con HTML del popup
        """
        estado_emoji = {
            'completed': '✅',
            'partial': '🟡',
            'pending': '🔴'
        }
        
        emoji = estado_emoji.get(ubicacion['estado'], '⚪')
        
        html = f"""
        <div style="font-family: Arial, sans-serif; min-width: 200px;">
            <h4 style="margin: 0 0 10px 0;">{emoji} {ubicacion['nombre']}</h4>
            <p style="margin: 5px 0;"><strong>Provincia:</strong> {ubicacion['provincia']}</p>
            <p style="margin: 5px 0;"><strong>Progreso:</strong> {ubicacion['porcentaje_completado']}%</p>
            <p style="margin: 5px 0;"><strong>Rubros:</strong> {ubicacion['rubros_completados']}/{ubicacion['total_rubros']}</p>
        </div>
        """
        
        return html
    
    def _empty_progress(self) -> Dict:
        """Retorna progreso vacío."""
        return {
            'total_combinaciones': self.total_combinaciones,
            'combinaciones_completadas': 0,
            'combinaciones_pendientes': self.total_combinaciones,
            'porcentaje_completado': 0,
            'porcentaje_pendiente': 100,
            'total_ubicaciones': len(self.ubicaciones_config),
            'ubicaciones_completas': 0,
            'ubicaciones_parciales': 0,
            'ubicaciones_sin_procesar': len(self.ubicaciones_config),
            'total_rubros': len(self.rubros_config),
            'porcentaje_ubicaciones_completas': 0,
            'porcentaje_ubicaciones_parciales': 0,
            'porcentaje_ubicaciones_sin_procesar': 100,
        }
