"""
Utilidades comunes para el scraper
"""
import time
import random
import logging
import pickle
import json
from datetime import datetime
from pathlib import Path


def setup_logging(log_dir='logs'):
    """Configura el sistema de logging al estilo Apify"""
    Path(log_dir).mkdir(exist_ok=True)
    
    log_file = Path(log_dir) / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)


def crear_directorios(config):
    """Crea los directorios necesarios para el proyecto"""
    directorios = [
        config['dir_resultados'],
        config['dir_backups'],
        config['dir_logs']
    ]
    
    for directorio in directorios:
        Path(directorio).mkdir(exist_ok=True)


def delay_aleatorio(rango):
    """Aplica un delay aleatorio dentro del rango especificado"""
    tiempo = random.uniform(rango[0], rango[1])
    time.sleep(tiempo)
    return tiempo


def guardar_cookies(driver, archivo):
    """Guarda las cookies de la sesión"""
    try:
        with open(archivo, 'wb') as f:
            pickle.dump(driver.get_cookies(), f)
        logging.info(f"Cookies guardadas en {archivo}")
    except Exception as e:
        logging.warning(f"Error guardando cookies: {str(e)}")


def cargar_cookies(driver, archivo):
    """Carga las cookies de una sesión anterior"""
    try:
        if Path(archivo).exists():
            with open(archivo, 'rb') as f:
                cookies = pickle.load(f)
                for cookie in cookies:
                    driver.add_cookie(cookie)
            logging.info(f"Cookies cargadas desde {archivo}")
            return True
    except Exception as e:
        logging.warning(f"Error cargando cookies: {str(e)}")
    return False


def guardar_estado(estado, archivo):
    """Guarda el estado de ejecución"""
    try:
        with open(archivo, 'w', encoding='utf-8') as f:
            json.dump(estado, f, indent=2, ensure_ascii=False)
        logging.info(f"Estado guardado: {estado['empresas_extraidas']} empresas")
    except Exception as e:
        logging.error(f"Error guardando estado: {str(e)}")


def cargar_estado(archivo):
    """Carga el estado de ejecución anterior"""
    try:
        if Path(archivo).exists():
            with open(archivo, 'r', encoding='utf-8') as f:
                estado = json.load(f)
            logging.info(f"Estado cargado: {estado['empresas_extraidas']} empresas previas")
            return estado
    except Exception as e:
        logging.warning(f"Error cargando estado: {str(e)}")
    
    # Retornar estado por defecto
    return {
        'rubros_completados': [],
        'segmentos_completados': {},
        'empresas_extraidas': 0,
        'ultimo_checkpoint': None,
        'fecha_inicio': datetime.now().isoformat()
    }


def ejecutar_con_reintentos(func, max_reintentos=3, descripcion="Operación"):
    """Ejecuta una función con reintentos en caso de error"""
    for intento in range(max_reintentos):
        try:
            return func()
        except Exception as e:
            logging.warning(f"{descripcion} - Intento {intento+1} fallado: {str(e)}")
            if intento < max_reintentos - 1:
                tiempo_espera = 10 * (intento + 1)
                logging.info(f"Reintentando en {tiempo_espera} segundos...")
                time.sleep(tiempo_espera)
            else:
                logging.error(f"{descripcion} - Todos los intentos fallaron")
                raise


def limpiar_texto(texto):
    """Limpia y normaliza texto extraído"""
    if not texto:
        return ""
    return texto.strip().replace('\n', ' ').replace('\r', ' ')


def extraer_google_maps_id(url):
    """
    Extrae el ID único de Google Maps de una URL
    
    Args:
        url (str): URL de Google Maps
        
    Returns:
        str: ID único de Google Maps o None si no se encuentra
    
    Ejemplos de formato:
        https://www.google.com/maps/place/.../1s0x95bcb7deea5eedeb:0x9fd8a41563d8c561!...
        El ID es: 0x95bcb7deea5eedeb:0x9fd8a41563d8c561
    """
    if not url:
        return None
    
    import re
    # Buscar el patrón del ID de Google Maps: 1s seguido de 0x...:0x...
    match = re.search(r'1s(0x[a-f0-9]+:0x[a-f0-9]+)', url)
    if match:
        return match.group(1)
    
    # Intentar con otro formato común: !3m... después de place_id
    match = re.search(r'place_id=([A-Za-z0-9_-]+)', url)
    if match:
        return match.group(1)
    
    return None


def generar_id_unico(nombre, direccion, url=None):
    """
    Genera un ID único para un lugar usando el ID de Google Maps (más confiable)
    o fallback a nombre + dirección
    
    Args:
        nombre (str): Nombre del lugar
        direccion (str): Dirección del lugar
        url (str, optional): URL de Google Maps
        
    Returns:
        str: ID único del lugar
    """
    # PRIORIDAD 1: Usar ID de Google Maps de la URL (más confiable)
    if url:
        google_id = extraer_google_maps_id(url)
        if google_id:
            return f"gmaps_{google_id}"
    
    # FALLBACK: Usar nombre + dirección (sin hash para consistencia)
    texto = f"{limpiar_texto(nombre)}_{limpiar_texto(direccion)}"
    return f"legacy_{texto}"


def formato_log_apify(rubro, coords, scroll, unique, duplicate, seen, paginations, out_of_location):
    """Genera un log en el formato estilo Apify"""
    lat, lng = coords
    return (f"🔍 [{rubro}][{lat:.4f}|{lng:.4f}][SCROLL: {scroll}]: "
            f"Search page scraped: {unique} unique, {duplicate} duplicate, "
            f"{seen} seen, {paginations} paginations, {out_of_location} outOfLocation.")
