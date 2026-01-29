#!/usr/bin/env python3
"""
Google Maps Scraper - Estrategia estilo Apify
Script principal para ejecutar el scraping de Google Maps

Uso:
    python main.py
    python main.py --ubicacion "Córdoba, Argentina" --rubros fabrica logistica
    
Controles:
    Ctrl+C - Pausar y guardar estado (presionar una vez)
"""
import sys
import logging
import argparse
import time
import random
import signal
from pathlib import Path
import undetected_chromedriver as uc

# Importar módulos propios
from config import CONFIG, USER_AGENTS
from utils import (
    setup_logging, crear_directorios, delay_aleatorio,
    guardar_cookies, cargar_cookies, guardar_estado, cargar_estado
)
from geolocator import Geolocator
from segment_searcher import SegmentSearcher
from data_manager import DataManager


# Variable global para manejar pausa
PAUSAR_SCRAPER = False

def signal_handler(sig, frame):
    """
    Maneja la señal Ctrl+C para pausar el scraper de forma segura
    """
    global PAUSAR_SCRAPER
    PAUSAR_SCRAPER = True
    print("\n\n" + "="*60)
    print("⏸️  PAUSA SOLICITADA - Guardando estado...")
    print("="*60)
    print("El scraper se detendrá después de completar el elemento actual.")
    print("NO presiones Ctrl+C nuevamente, espera a que termine de guardar.")
    print("="*60 + "\n")


class GoogleMapsScraper:
    def __init__(self, config):
        self.config = config
        self.driver = None
        self.geolocator = Geolocator()
        self.data_manager = DataManager(config)
        self.estado = cargar_estado(config['archivo_estado'])
        
    def inicializar_driver(self):
        """
        Inicializa el driver de Selenium con configuración anti-detección
        """
        logging.info("🚀 Inicializando navegador...")
        
        try:
            # Configurar opciones básicas
            options = uc.ChromeOptions()
            
            # Configuraciones básicas
            if not self.config['headless']:
                options.add_argument('--start-maximized')
            else:
                options.add_argument('--headless=new')
            
            # Argumentos para estabilidad
            options.add_argument('--disable-dev-shm-usage')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-gpu')
            options.add_argument(f'user-agent={USER_AGENTS[0]}')
            
            # Preferencias simples
            prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.default_content_setting_values.notifications": 2
            }
            options.add_experimental_option("prefs", prefs)
            
            # Inicializar driver con undetected-chromedriver
            # undetected-chromedriver maneja automáticamente la anti-detección
            # version_main=144 fuerza a usar Chrome 144
            self.driver = uc.Chrome(options=options, use_subprocess=True, version_main=144)
            
            logging.info("✅ Navegador inicializado correctamente")
            
            # Cargar cookies si existen
            self.driver.get("https://www.google.com/maps")
            cargar_cookies(self.driver, self.config['archivo_cookies'])
            
            return True
            
        except Exception as e:
            logging.error(f"❌ Error inicializando navegador: {str(e)}")
            return False
    
    def ejecutar(self):
        """
        Ejecuta el proceso completo de scraping
        """
        try:
            # Crear directorios necesarios
            crear_directorios(self.config)
            
            # Inicializar driver
            if not self.inicializar_driver():
                logging.error("No se pudo inicializar el navegador")
                return False
            
            # Determinar ubicaciones a procesar
            ubicaciones = self.config.get('ubicaciones', [self.config.get('ubicacion')])
            
            logging.info(f"\n{'='*60}")
            logging.info(f"🌎 UBICACIONES A PROCESAR: {len(ubicaciones)}")
            logging.info(f"{'='*60}")
            for idx, ubi in enumerate(ubicaciones, 1):
                logging.info(f"  {idx}. {ubi}")
            
            # Iterar por cada ubicación
            for idx_ubicacion, ubicacion in enumerate(ubicaciones, 1):
                logging.info(f"\n{'#'*60}")
                logging.info(f"🌍 UBICACIÓN {idx_ubicacion}/{len(ubicaciones)}: {ubicacion}")
                logging.info(f"{'#'*60}")
                
                # Crear ID único para esta ubicación (para tracking)
                ubicacion_id = ubicacion.replace(", ", "_").replace(" ", "_").lower()
                
                # Verificar si esta ubicación ya fue completada
                ubicaciones_completadas = self.estado.get('ubicaciones_completadas', {})
                if ubicacion_id in ubicaciones_completadas and ubicaciones_completadas[ubicacion_id].get('completado'):
                    logging.info(f"⏭️  {ubicacion} ya fue completada previamente")
                    continue
                
                # Paso 1: Geolocalización para esta ubicación
                logging.info(f"\n{'='*60}")
                logging.info(f"📍 PASO 1: GEOLOCALIZACIÓN - {ubicacion}")
                logging.info(f"{'='*60}")
                
                polygon, bbox = self.geolocator.obtener_poligono_ubicacion(ubicacion)
                
                if not polygon:
                    logging.error(f"No se pudo geolocalizar: {ubicacion}")
                    continue
                
                # Paso 2: División en segmentos para esta ubicación
                logging.info(f"\n{'='*60}")
                logging.info(f"📐 PASO 2: DIVISIÓN EN SEGMENTOS - {ubicacion}")
                logging.info(f"{'='*60}")
                
                segmentos = self.geolocator.dividir_poligono_en_segmentos(
                    polygon, 
                    self.config['grid_size']
                )
                
                logging.info(f"✅ Área dividida en {len(segmentos)} segmentos")
                
                # Paso 3: Búsqueda por segmento y rubro en esta ubicación
                logging.info(f"\n{'='*60}")
                logging.info(f"🔍 PASO 3: BÚSQUEDA - {ubicacion}")
                logging.info(f"{'='*60}")
                
                searcher = SegmentSearcher(self.driver, self.config)
                rubros = self.config['rubros']
                
                total_segmentos = len(segmentos)
                total_rubros = len(rubros)
                
                logging.info(f"Total de búsquedas en {ubicacion}: {total_segmentos * total_rubros}")
                logging.info(f"Rubros: {len(rubros)} rubros configurados")
                
                # Inicializar tracking de rubros para esta ubicación
                if ubicacion_id not in self.estado.get('ubicaciones_completadas', {}):
                    self.estado.setdefault('ubicaciones_completadas', {})[ubicacion_id] = {
                        'nombre': ubicacion,
                        'rubros_completados': [],
                        'completado': False
                    }
                
                rubros_completados_ubicacion = self.estado['ubicaciones_completadas'][ubicacion_id].get('rubros_completados', [])
                rubros_pendientes_ubicacion = [r for r in rubros if r not in rubros_completados_ubicacion]
                
                if not rubros_pendientes_ubicacion:
                    logging.info(f"✅ Todos los rubros ya fueron procesados en {ubicacion}")
                    self.estado['ubicaciones_completadas'][ubicacion_id]['completado'] = True
                    continue
                
                logging.info(f"📋 Rubros pendientes en {ubicacion}: {len(rubros_pendientes_ubicacion)}")
                
                # Iterar por cada segmento en esta ubicación
                for idx_segmento, segmento in enumerate(segmentos, 1):
                    logging.info(f"\n{'─'*60}")
                    logging.info(f"📍 {ubicacion} - SEGMENTO {idx_segmento}/{total_segmentos}")
                    logging.info(f"   Centro: {segmento['centro']}")
                    logging.info(f"{'─'*60}")
                    
                    # Iterar por rubros pendientes en esta ubicación
                    for idx_rubro, rubro in enumerate(rubros_pendientes_ubicacion, 1):
                        # 🔴 VERIFICAR SI SE SOLICITÓ PAUSA
                        global PAUSAR_SCRAPER
                        if PAUSAR_SCRAPER:
                            logging.info("\n⏸️  PAUSA DETECTADA - Guardando progreso...")
                            
                            # Guardar estado actual
                            self.estado['ubicaciones_completadas'][ubicacion_id]['rubros_completados'] = rubros_completados_ubicacion
                            self.estado['empresas_extraidas'] = self.data_manager.total_empresas
                            guardar_estado(self.estado, self.config['archivo_estado'])
                            
                            # Guardar datos
                            self.data_manager.guardar_checkpoint()
                            
                            logging.info("\n" + "="*60)
                            logging.info("✅ ESTADO GUARDADO CORRECTAMENTE")
                            logging.info("="*60)
                            logging.info(f"📊 Progreso guardado:")
                            logging.info(f"   - Ciudad actual: {ubicacion}")
                            logging.info(f"   - Rubros completados en {ubicacion}: {len(rubros_completados_ubicacion)}/{len(rubros)}")
                            logging.info(f"   - Total empresas: {self.data_manager.total_empresas}")
                            logging.info(f"\n💡 Para reanudar, ejecuta nuevamente: python main.py")
                            logging.info("="*60 + "\n")
                            
                            return False  # Salir del scraper
                        
                        logging.info(f"\n🏷️  Rubro {idx_rubro}/{len(rubros_pendientes_ubicacion)}: {rubro}")
                        
                        try:
                            # Buscar en el segmento
                            resultados = searcher.buscar_en_segmento(rubro, segmento)
                            
                            # Agregar resultados
                            if resultados:
                                # Agregar ciudad a cada resultado
                                for resultado in resultados:
                                    resultado['ciudad'] = ubicacion
                                
                                self.data_manager.agregar_lugares(resultados)
                            
                            # Marcar rubro como completado para esta ubicación
                            if rubro not in rubros_completados_ubicacion:
                                rubros_completados_ubicacion.append(rubro)
                            
                            # 🔴 GUARDAR ESTADO DESPUÉS DE CADA RUBRO (para poder reanudar)
                            self.estado['ubicaciones_completadas'][ubicacion_id]['rubros_completados'] = rubros_completados_ubicacion
                            self.estado['empresas_extraidas'] = self.data_manager.total_empresas
                            guardar_estado(self.estado, self.config['archivo_estado'])
                            
                            # Delay entre rubros
                            if idx_rubro < len(rubros_pendientes_ubicacion):
                                tiempo = delay_aleatorio(self.config['delays']['entre_rubros'])
                                logging.info(f"⏳ Esperando {tiempo:.1f}s antes del siguiente rubro...")
                            
                        except Exception as e:
                            logging.error(f"❌ Error procesando rubro '{rubro}': {str(e)}")
                            continue
                    
                    # Delay entre segmentos
                    if idx_segmento < total_segmentos:
                        tiempo = delay_aleatorio(self.config['delays']['entre_segmentos'])
                        logging.info(f"⏳ Esperando {tiempo:.1f}s antes del siguiente segmento...")
                
                # Actualizar estado de ubicación
                self.estado['ubicaciones_completadas'][ubicacion_id]['rubros_completados'] = rubros_completados_ubicacion
                self.estado['ubicaciones_completadas'][ubicacion_id]['completado'] = (len(rubros_completados_ubicacion) >= len(rubros))
                
                # Guardar estado
                self.estado['empresas_extraidas'] = self.data_manager.total_empresas
                guardar_estado(self.estado, self.config['archivo_estado'])
                
                logging.info(f"\n✅ {ubicacion} completada - {len(rubros_completados_ubicacion)}/{len(rubros)} rubros")
                
                # Delay entre ubicaciones (importante para no ser detectado)
                if idx_ubicacion < len(ubicaciones):
                    tiempo_espera = random.uniform(15, 30)
                    logging.info(f"\n⏳ Esperando {tiempo_espera:.1f}s antes de la siguiente ciudad...")
                    time.sleep(tiempo_espera)
            
            # Paso 4: Guardar datos finales
            logging.info(f"\n{'='*60}")
            logging.info(f"💾 PASO 4: GUARDANDO DATOS FINALES")
            logging.info(f"{'='*60}")
            
            self.data_manager.guardar_final()
            
            # Guardar cookies para futuros usos
            guardar_cookies(self.driver, self.config['archivo_cookies'])
            
            logging.info(f"\n{'='*60}")
            logging.info(f"✅ PROCESO COMPLETADO EXITOSAMENTE")
            logging.info(f"{'='*60}")
            
            return True
            
        except KeyboardInterrupt:
            logging.warning("\n⚠️  Proceso interrumpido por el usuario")
            self.data_manager.guardar_checkpoint()
            guardar_estado(self.estado, self.config['archivo_estado'])
            return False
            
        except Exception as e:
            logging.error(f"❌ Error en el proceso principal: {str(e)}", exc_info=True)
            self.data_manager.guardar_checkpoint()
            return False
            
        finally:
            # Cerrar navegador
            if self.driver:
                logging.info("🔒 Cerrando navegador...")
                self.driver.quit()


def parse_arguments():
    """
    Parsea los argumentos de línea de comandos
    """
    parser = argparse.ArgumentParser(
        description='Google Maps Scraper con estrategia estilo Apify'
    )
    
    parser.add_argument(
        '--ubicacion',
        type=str,
        help='Ubicación a buscar (ej: "Córdoba, Argentina")'
    )
    
    parser.add_argument(
        '--rubros',
        nargs='+',
        help='Rubros a buscar (ej: fabrica logistica transportes)'
    )
    
    parser.add_argument(
        '--grid-size',
        type=int,
        help='Tamaño de la cuadrícula para dividir el área (default: 2)'
    )
    
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Ejecutar en modo headless (sin interfaz gráfica)'
    )
    
    return parser.parse_args()


def main():
    """
    Función principal
    """
    # 🔴 CONFIGURAR MANEJADOR DE CTRL+C PARA PAUSA SEGURA
    signal.signal(signal.SIGINT, signal_handler)
    
    # Configurar logging
    logger = setup_logging(CONFIG['dir_logs'])
    
    # Parsear argumentos
    args = parse_arguments()
    
    # Actualizar configuración con argumentos
    if args.ubicacion:
        CONFIG['ubicacion'] = args.ubicacion
    
    if args.rubros:
        CONFIG['rubros'] = args.rubros
    
    if args.grid_size:
        CONFIG['grid_size'] = args.grid_size
    
    if args.headless:
        CONFIG['headless'] = True
    
    # Banner inicial
    logger.info("\n" + "="*60)
    logger.info("🗺️  GOOGLE MAPS SCRAPER - ESTRATEGIA APIFY")
    logger.info("="*60)
    logger.info(f"📍 Ubicaciones: {len(CONFIG.get('ubicaciones', [CONFIG.get('ubicacion')]))} ciudades")
    logger.info(f"🏷️  Rubros: {len(CONFIG['rubros'])} rubros")
    logger.info(f"📐 Grid size: {CONFIG['grid_size']}x{CONFIG['grid_size']}")
    logger.info(f"💾 Checkpoint cada: {CONFIG['checkpoint_cada']} empresas")
    logger.info("\n⏸️  CTRL+C para pausar y guardar (presiona solo una vez)")
    logger.info("="*60 + "\n")
    
    # Ejecutar scraper
    scraper = GoogleMapsScraper(CONFIG)
    success = scraper.ejecutar()
    
    if success:
        logger.info("\n✅ Script finalizado exitosamente")
        sys.exit(0)
    else:
        logger.info("\n⏸️  Script pausado - ejecuta nuevamente para reanudar")
        sys.exit(0)


if __name__ == "__main__":
    main()
