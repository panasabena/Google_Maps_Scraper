"""
Módulo de geolocalización y división de área
Usa Nominatim (OpenStreetMap) para convertir ubicación en polígono
y divide el área en segmentos para cobertura completa
"""
import logging
import requests
from shapely.geometry import shape, box, Point
from shapely.ops import unary_union
import time


class Geolocator:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org"
        self.headers = {
            'User-Agent': 'GoogleMapsScraper/1.0 (Educational Purpose)'
        }
    
    def obtener_poligono_ubicacion(self, ubicacion):
        """
        Convierte una ubicación textual en un polígono de coordenadas
        
        Args:
            ubicacion (str): Nombre de la ubicación (ej: "Córdoba, Argentina")
            
        Returns:
            tuple: (polygon, boundingbox) o (None, None) si falla
        """
        logging.info(f"📡 Geolocalizando: {ubicacion}")
        
        url = f"{self.base_url}/search"
        params = {
            'q': ubicacion,
            'format': 'json',
            'polygon_geojson': 1,
            'limit': 1
        }
        
        try:
            response = requests.get(url, params=params, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                logging.error(f"No se encontró la ubicación: {ubicacion}")
                return None, None
            
            resultado = data[0]
            
            # Extraer polígono si está disponible
            if 'geojson' in resultado:
                polygon = shape(resultado['geojson'])
                boundingbox = resultado.get('boundingbox', [])
                
                logging.info(f"✅ Ubicación encontrada: {resultado.get('display_name', ubicacion)}")
                logging.info(f"   Bounding box: {boundingbox}")
                
                return polygon, boundingbox
            else:
                # Si no hay polígono, crear uno desde el bounding box
                bbox = resultado['boundingbox']
                # bbox format: [min_lat, max_lat, min_lon, max_lon]
                min_lat, max_lat, min_lon, max_lon = map(float, bbox)
                polygon = box(min_lon, min_lat, max_lon, max_lat)
                
                logging.info(f"✅ Ubicación encontrada (usando bounding box): {resultado.get('display_name', ubicacion)}")
                
                return polygon, bbox
                
        except requests.RequestException as e:
            logging.error(f"Error en la solicitud de geolocalización: {str(e)}")
            return None, None
        except Exception as e:
            logging.error(f"Error procesando datos de geolocalización: {str(e)}")
            return None, None
    
    def dividir_poligono_en_segmentos(self, polygon, grid_size=2):
        """
        Divide un polígono en una cuadrícula de segmentos
        
        Args:
            polygon: Polígono de Shapely
            grid_size (int): Tamaño de la cuadrícula (ej: 2 = 2x2 = 4 segmentos)
            
        Returns:
            list: Lista de diccionarios con información de cada segmento
        """
        logging.info(f"📐 Dividiendo área en cuadrícula de {grid_size}x{grid_size}")
        
        minx, miny, maxx, maxy = polygon.bounds
        
        segmentos = []
        x_step = (maxx - minx) / grid_size
        y_step = (maxy - miny) / grid_size
        
        segment_id = 0
        for i in range(grid_size):
            for j in range(grid_size):
                x1 = minx + i * x_step
                x2 = minx + (i + 1) * x_step
                y1 = miny + j * y_step
                y2 = miny + (j + 1) * y_step
                
                segment_box = box(x1, y1, x2, y2)
                
                # Solo incluir segmentos que intersecten con el polígono original
                if segment_box.intersects(polygon):
                    centro = segment_box.centroid
                    
                    segmento = {
                        'id': segment_id,
                        'bounds': (x1, y1, x2, y2),
                        'centro': (centro.y, centro.x),  # (lat, lng) - orden correcto para Google Maps
                        'box': segment_box,
                        'area': segment_box.area
                    }
                    
                    segmentos.append(segmento)
                    segment_id += 1
                    
                    logging.info(f"   Segmento {segment_id}: Centro ({centro.y:.4f}, {centro.x:.4f})")
        
        logging.info(f"✅ Creados {len(segmentos)} segmentos")
        
        return segmentos
    
    def punto_esta_en_segmento(self, lat, lng, segmento):
        """
        Verifica si un punto está dentro de un segmento
        
        Args:
            lat (float): Latitud del punto
            lng (float): Longitud del punto
            segmento (dict): Diccionario con información del segmento
            
        Returns:
            bool: True si el punto está dentro del segmento
        """
        punto = Point(lng, lat)  # Shapely usa (x, y) = (lng, lat)
        return segmento['box'].contains(punto)


def test_geolocator():
    """Función de prueba para el geolocalizador"""
    geolocator = Geolocator()
    
    # Prueba 1: Geolocalizar Córdoba, Argentina
    ubicacion = "Córdoba, Argentina"
    polygon, bbox = geolocator.obtener_poligono_ubicacion(ubicacion)
    
    if polygon:
        print(f"\n✅ Geolocalización exitosa")
        print(f"   Área del polígono: {polygon.area:.6f} grados cuadrados")
        
        # Prueba 2: Dividir en segmentos
        segmentos = geolocator.dividir_poligono_en_segmentos(polygon, grid_size=2)
        print(f"\n✅ División en segmentos exitosa")
        print(f"   Total de segmentos: {len(segmentos)}")
        
        for seg in segmentos:
            print(f"   - Segmento {seg['id']}: Centro {seg['centro']}")
    else:
        print(f"\n❌ Error en la geolocalización")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    test_geolocator()
