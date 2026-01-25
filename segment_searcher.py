"""
Módulo de búsqueda por segmento
Realiza búsquedas en Google Maps para un segmento geográfico específico
y maneja el scroll infinito para obtener todos los resultados
"""
import logging
import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import SELECTORS
from utils import delay_aleatorio, generar_id_unico, formato_log_apify
from detail_extractor import DetailExtractor


class SegmentSearcher:
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
        self.wait = WebDriverWait(driver, 15)
        self.extractor = DetailExtractor(driver)
    
    def construir_url_busqueda(self, rubro, segmento):
        """
        Construye la URL de búsqueda para un rubro y segmento específico
        
        Args:
            rubro (str): Rubro a buscar (ej: "fabrica")
            segmento (dict): Información del segmento geográfico
            
        Returns:
            str: URL de búsqueda en Google Maps
        """
        lat, lng = segmento['centro']
        zoom = self.config['zoom_level']
        
        # Codificar el rubro para URL
        rubro_encoded = rubro.replace(' ', '+')
        
        url = f"https://www.google.com/maps/search/{rubro_encoded}/@{lat},{lng},{zoom}z?hl=es-419"
        
        return url
    
    def manejar_consentimiento(self):
        """
        Maneja la pantalla de consentimiento/cookies si aparece
        """
        try:
            # Intentar con diferentes selectores
            for selector in [SELECTORS['consent_button'], SELECTORS['consent_button_alt']]:
                try:
                    consent_button = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    consent_button.click()
                    logging.info("✅ [CONSENT SCREEN] handled")
                    time.sleep(2)
                    return True
                except TimeoutException:
                    continue
        except Exception as e:
            logging.debug(f"No se detectó pantalla de consentimiento: {str(e)}")
        
        return False
    
    def detectar_fin_resultados(self):
        """
        Detecta si se llegó al final de los resultados
        
        Returns:
            bool: True si se llegó al final
        """
        try:
            # Buscar mensaje de fin
            mensaje_fin = self.driver.find_element(By.XPATH, SELECTORS['mensaje_fin'])
            if mensaje_fin.is_displayed():
                return True
        except NoSuchElementException:
            pass
        
        return False
    
    def hacer_scroll(self, elemento_feed):
        """
        Hace scroll en el feed de resultados para cargar más elementos
        Usa múltiples estrategias para mayor confiabilidad
        
        Args:
            elemento_feed: WebElement del contenedor de resultados
            
        Returns:
            bool: True si se pudo hacer scroll exitosamente
        """
        try:
            # Obtener número de elementos actual
            elementos_antes = len(self.driver.find_elements(By.XPATH, SELECTORS['lugar_elemento']))
            
            # ESTRATEGIA 1: Scroll al último elemento
            try:
                elementos = self.driver.find_elements(By.XPATH, SELECTORS['lugar_elemento'])
                if elementos:
                    ultimo = elementos[-1]
                    self.driver.execute_script(
                        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'end'});", 
                        ultimo
                    )
                    time.sleep(1.5)
            except:
                pass
            
            # ESTRATEGIA 2: Scroll en el contenedor feed
            try:
                # Obtener posición actual de scroll
                scroll_actual = self.driver.execute_script("return arguments[0].scrollTop", elemento_feed)
                
                # Scroll 800px hacia abajo
                self.driver.execute_script(
                    "arguments[0].scrollTop = arguments[0].scrollTop + 800;",
                    elemento_feed
                )
                time.sleep(1.5)
                
                # Verificar que realmente scrolleó
                scroll_nuevo = self.driver.execute_script("return arguments[0].scrollTop", elemento_feed)
                
                if scroll_nuevo <= scroll_actual:
                    # Si no scrolleó, intentar con scrollBy
                    self.driver.execute_script(
                        "arguments[0].scrollBy(0, 1000);",
                        elemento_feed
                    )
                    time.sleep(1.5)
            except:
                pass
            
            # ESTRATEGIA 3: Enviar teclas (backup)
            try:
                from selenium.webdriver.common.keys import Keys
                elemento_feed.send_keys(Keys.PAGE_DOWN)
                time.sleep(1)
            except:
                pass
            
            # Esperar a que carguen nuevos elementos
            delay_aleatorio(self.config['delays']['despues_scroll'])
            
            # Obtener número de elementos después del scroll
            elementos_despues = len(self.driver.find_elements(By.XPATH, SELECTORS['lugar_elemento']))
            
            # Log de progreso
            if elementos_despues > elementos_antes:
                logging.debug(f"   Scroll exitoso: {elementos_antes} → {elementos_despues} elementos")
                return True
            else:
                logging.debug(f"   Scroll sin cambios: {elementos_antes} elementos")
                return False
            
        except Exception as e:
            logging.debug(f"Error haciendo scroll: {str(e)}")
            return False
    
    def extraer_resultados_pagina(self, rubro, segmento):
        """
        Extrae todos los resultados de una página con scroll infinito
        
        Args:
            rubro (str): Rubro buscado
            segmento (dict): Información del segmento
            
        Returns:
            list: Lista de diccionarios con datos de lugares
        """
        lugares = []
        seen_ids = set()
        pagination_count = 0
        duplicate_count = 0
        out_of_location_count = 0
        scrolls_sin_cambio = 0
        max_scrolls_sin_cambio = 5  # Aumentado de 3 a 5
        
        try:
            # Esperar a que aparezca el feed de resultados
            elemento_feed = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, SELECTORS['resultados_feed']))
            )
            
            logging.info(f"📄 Iniciando extracción para rubro: {rubro}")
            
            elementos_anteriores = 0
            
            while pagination_count < self.config['max_scrolls_por_pagina']:
                try:
                    # Extraer elementos visibles
                    elementos = self.driver.find_elements(By.XPATH, SELECTORS['lugar_elemento'])
                    
                    if not elementos:
                        logging.warning("No se encontraron elementos en la página")
                        break
                    
                    logging.info(f"   Scroll {pagination_count + 1}: {len(elementos)} elementos en página")
                    
                    # Procesar cada elemento
                    nuevos_en_esta_ronda = 0
                    for elemento in elementos:
                        try:
                            # Extraer datos básicos
                            datos = self.extractor.extraer_datos_basicos(elemento)
                            
                            if not datos['nombre']:
                                continue
                            
                            # Generar ID único
                            lugar_id = generar_id_unico(datos['nombre'], datos['direccion'])
                            
                            if lugar_id not in seen_ids:
                                seen_ids.add(lugar_id)
                                
                                # Agregar metadatos
                                datos['rubro_buscado'] = rubro
                                datos['segmento_id'] = segmento['id']
                                datos['segmento_centro'] = segmento['centro']
                                
                                # Normalizar datos
                                datos = self.extractor.normalizar_datos(datos)
                                
                                lugares.append(datos)
                                nuevos_en_esta_ronda += 1
                            else:
                                duplicate_count += 1
                                
                        except Exception as e:
                            logging.debug(f"Error procesando elemento: {str(e)}")
                            continue
                    
                    # Log de progreso
                    if nuevos_en_esta_ronda > 0:
                        logging.info(f"   ✅ {nuevos_en_esta_ronda} nuevos, {len(lugares)} total")
                        scrolls_sin_cambio = 0  # Resetear contador
                    else:
                        scrolls_sin_cambio += 1
                        logging.info(f"   ⚠️  Sin nuevos elementos ({scrolls_sin_cambio}/{max_scrolls_sin_cambio})")
                    
                    # Si no hay nuevos elementos después de varios scrolls, terminar
                    if scrolls_sin_cambio >= max_scrolls_sin_cambio:
                        logging.info("   🛑 Sin nuevos elementos después de múltiples scrolls")
                        break
                    
                    # Verificar si llegamos al final
                    if self.detectar_fin_resultados():
                        logging.info("✅ Se detectó el final de los resultados")
                        break
                    
                    # Hacer scroll más agresivo
                    # Scroll al último elemento visible
                    if elementos:
                        try:
                            ultimo = elementos[-1]
                            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", ultimo)
                            delay_aleatorio((1, 2))
                            
                            # Scroll adicional hacia abajo
                            self.driver.execute_script(
                                "arguments[0].scrollBy(0, 500);",
                                elemento_feed
                            )
                        except:
                            pass
                    
                    # Esperar a que carguen nuevos elementos
                    delay_aleatorio(self.config['delays']['despues_scroll'])
                    
                    pagination_count += 1
                    
                except Exception as e:
                    logging.warning(f"Error en iteración de scroll: {str(e)}")
                    break
            
            # Log final estilo Apify
            log_msg = formato_log_apify(
                rubro=rubro,
                coords=segmento['centro'],
                scroll=pagination_count,
                unique=len(lugares),
                duplicate=duplicate_count,
                seen=len(seen_ids),
                paginations=pagination_count,
                out_of_location=out_of_location_count
            )
            logging.info(log_msg)
            
        except TimeoutException:
            logging.error(f"Timeout esperando resultados para {rubro}")
        except Exception as e:
            logging.error(f"Error extrayendo resultados: {str(e)}")
        
        return lugares
    
    def buscar_en_segmento(self, rubro, segmento):
        """
        Realiza una búsqueda completa en un segmento para un rubro
        
        Args:
            rubro (str): Rubro a buscar
            segmento (dict): Información del segmento
            
        Returns:
            list: Lista de lugares encontrados
        """
        try:
            # Construir URL
            url = self.construir_url_busqueda(rubro, segmento)
            logging.info(f"\n🔍 Buscando '{rubro}' en segmento {segmento['id']}")
            logging.info(f"   URL: {url}")
            
            # Navegar a la URL
            self.driver.get(url)
            
            # Delay inicial
            delay_aleatorio(self.config['delays']['carga_inicial'])
            
            # Manejar consentimiento si aparece
            self.manejar_consentimiento()
            
            # Esperar un poco más después del consentimiento
            time.sleep(2)
            
            # Extraer resultados
            resultados = self.extraer_resultados_pagina(rubro, segmento)
            
            logging.info(f"✅ Extracción completada: {len(resultados)} lugares encontrados")
            
            return resultados
            
        except Exception as e:
            logging.error(f"Error en búsqueda de segmento: {str(e)}")
            return []
