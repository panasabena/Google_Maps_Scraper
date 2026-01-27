"""
Módulo de extracción de detalles de lugares
Extrae información detallada de cada negocio/lugar de Google Maps
"""
import logging
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from config import SELECTORS, DETAIL_SELECTORS
from utils import limpiar_texto, delay_aleatorio


class DetailExtractor:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def extraer_datos_basicos(self, elemento):
        """
        Extrae datos básicos de un elemento de la lista de resultados
        sin hacer clic en él
        
        Args:
            elemento: WebElement de Selenium
            
        Returns:
            dict: Diccionario con los datos extraídos
        """
        datos = {
            'nombre': '',
            'direccion': '',
            'categoria': '',
            'rating': '',
            'num_resenas': '',
            'telefono': '',
            'sitio_web': '',
            'url_google_maps': '',
            'latitud': '',
            'longitud': ''
        }
        
        try:
            # Nombre
            try:
                nombre_elem = elemento.find_element(By.XPATH, SELECTORS['nombre'])
                datos['nombre'] = limpiar_texto(nombre_elem.text)
            except NoSuchElementException:
                pass
            
            # URL de Google Maps y coordenadas
            try:
                link_elem = elemento.find_element(By.XPATH, SELECTORS['lugar_link'])
                url = link_elem.get_attribute('href')
                datos['url_google_maps'] = url
                
                # Extraer coordenadas de la URL si es posible
                # Formato: /maps/place/.../@lat,lng,zoom...
                match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+)', url)
                if match:
                    datos['latitud'] = match.group(1)
                    datos['longitud'] = match.group(2)
            except NoSuchElementException:
                pass
            
            # Dirección
            try:
                direccion_elem = elemento.find_element(By.XPATH, SELECTORS['direccion_breve'])
                datos['direccion'] = limpiar_texto(direccion_elem.text)
            except NoSuchElementException:
                pass
            
            # Rating
            try:
                rating_elem = elemento.find_element(By.XPATH, SELECTORS['rating'])
                datos['rating'] = limpiar_texto(rating_elem.text)
            except NoSuchElementException:
                pass
            
            # Número de reseñas
            try:
                resenas_elem = elemento.find_element(By.XPATH, SELECTORS['num_resenas'])
                datos['num_resenas'] = limpiar_texto(resenas_elem.text).replace('(', '').replace(')', '')
            except NoSuchElementException:
                pass
            
            # Categoría
            try:
                categoria_elem = elemento.find_element(By.XPATH, SELECTORS['categoria'])
                datos['categoria'] = limpiar_texto(categoria_elem.text)
            except NoSuchElementException:
                pass
            
            # Teléfono (intentar extraer de la lista)
            telefono_encontrado = False
            try:
                telefono_elem = elemento.find_element(By.XPATH, SELECTORS['telefono_lista'])
                datos['telefono'] = limpiar_texto(telefono_elem.get_attribute('aria-label').replace('Teléfono:', '').replace('Phone:', '').strip())
                telefono_encontrado = True
            except NoSuchElementException:
                # Intentar extraer del HTML directamente
                try:
                    html = elemento.get_attribute('innerHTML')
                    telefono = self.extraer_telefono_de_html_texto(html)
                    if telefono:
                        datos['telefono'] = telefono
                        telefono_encontrado = True
                except:
                    pass
            
            # Si no se encontró teléfono, marcar como N/A
            if not telefono_encontrado or not datos['telefono']:
                datos['telefono'] = 'N/A'
            
            # Sitio web y email dejar vacíos si no existen (NO poner N/A)
            # El usuario solo quiere N/A en teléfono
            
        except Exception as e:
            logging.debug(f"Error extrayendo datos básicos: {str(e)}")
        
        return datos
    
    def extraer_telefono_de_html_texto(self, html):
        """
        Extrae número de teléfono del HTML
        
        Args:
            html: HTML como string
            
        Returns:
            str: Número de teléfono encontrado o cadena vacía
        """
        try:
            # Patrones comunes de teléfonos argentinos y generales
            patrones = [
                r'\+54\s?\d{1,4}\s?\d{3,4}[-\s]?\d{4}',  # +54 351 1234567
                r'\+\d{1,3}\s?\d{1,4}\s?\d{3,4}[-\s]?\d{4}',  # Internacional
                r'0\d{3,4}[-\s]?\d{3,4}[-\s]?\d{4}',  # 0351 1234567
                r'\d{3,4}[-\s]\d{3,4}[-\s]\d{4}',  # 351-123-4567
                r'\(\d{3,4}\)\s?\d{3,4}[-\s]?\d{4}'  # (351) 1234567
            ]
            
            for patron in patrones:
                match = re.search(patron, html)
                if match:
                    return match.group(0).strip()
                    
        except Exception as e:
            logging.debug(f"Error buscando teléfono en HTML: {str(e)}")
        
        return ''
    
    def extraer_datos_detallados(self, url_lugar):
        """
        Extrae datos detallados haciendo clic en un lugar específico
        (Usar solo si se necesitan datos adicionales no disponibles en la lista)
        
        Args:
            url_lugar (str): URL del lugar en Google Maps
            
        Returns:
            dict: Diccionario con datos detallados adicionales
        """
        datos_detallados = {
            'telefono': '',
            'sitio_web': '',
            'email': '',
            'horarios': '',
            'rango_precios': '',
            'direccion_completa': '',
            'latitud': '',
            'longitud': ''
        }
        
        try:
            # Navegar a la página del lugar
            self.driver.get(url_lugar)
            delay_aleatorio((2, 4))
            
            # Extraer coordenadas de la URL actual (más precisa después de cargar)
            try:
                url_actual = self.driver.current_url
                # Buscar patrón: @latitud,longitud,zoom
                match = re.search(r'@(-?\d+\.\d+),(-?\d+\.\d+),', url_actual)
                if match:
                    datos_detallados['latitud'] = match.group(1)
                    datos_detallados['longitud'] = match.group(2)
            except Exception as e:
                logging.debug(f"No se pudieron extraer coordenadas de URL: {str(e)}")
            
            # Teléfono
            try:
                telefono_elem = self.wait.until(
                    EC.presence_of_element_located((By.XPATH, DETAIL_SELECTORS['telefono']))
                )
                datos_detallados['telefono'] = limpiar_texto(telefono_elem.text)
            except TimeoutException:
                datos_detallados['telefono'] = 'N/A'  # Solo N/A en teléfono
            
            # Sitio web - dejar vacío si no existe
            try:
                web_elem = self.driver.find_element(By.XPATH, DETAIL_SELECTORS['sitio_web'])
                datos_detallados['sitio_web'] = web_elem.get_attribute('href')
            except NoSuchElementException:
                pass  # Dejar vacío
            
            # Email - dejar vacío si no existe
            try:
                email_elem = self.driver.find_element(By.XPATH, DETAIL_SELECTORS['email'])
                email_href = email_elem.get_attribute('href')
                if 'mailto:' in email_href:
                    datos_detallados['email'] = email_href.replace('mailto:', '')
            except NoSuchElementException:
                pass  # Dejar vacío
            
            # Dirección completa
            try:
                direccion_elem = self.driver.find_element(By.XPATH, DETAIL_SELECTORS['direccion_completa'])
                datos_detallados['direccion_completa'] = limpiar_texto(direccion_elem.text)
            except NoSuchElementException:
                pass
            
            # Horarios
            try:
                horarios_elem = self.driver.find_element(By.XPATH, DETAIL_SELECTORS['horarios'])
                datos_detallados['horarios'] = limpiar_texto(horarios_elem.get_attribute('aria-label'))
            except NoSuchElementException:
                pass
            
        except Exception as e:
            logging.warning(f"Error extrayendo datos detallados de {url_lugar}: {str(e)}")
        
        return datos_detallados
    
    def extraer_telefono_de_html(self, elemento):
        """
        Intenta extraer número de teléfono del HTML del elemento
        
        Args:
            elemento: WebElement de Selenium
            
        Returns:
            str: Número de teléfono encontrado o cadena vacía
        """
        try:
            html = elemento.get_attribute('innerHTML')
            
            # Patrones comunes de teléfonos argentinos
            patrones = [
                r'\+54\s?\d{1,4}\s?\d{3,4}\s?\d{4}',  # +54 351 1234567
                r'0\d{3,4}\s?\d{3,4}\s?\d{4}',  # 0351 1234567
                r'\d{3,4}\s?\d{3,4}\s?\d{4}',  # 351 1234567
                r'\(\d{3,4}\)\s?\d{3,4}-?\d{4}'  # (351) 1234567
            ]
            
            for patron in patrones:
                match = re.search(patron, html)
                if match:
                    return match.group(0)
                    
        except Exception as e:
            logging.debug(f"Error buscando teléfono en HTML: {str(e)}")
        
        return ''
    
    def normalizar_datos(self, datos):
        """
        Normaliza y limpia los datos extraídos
        
        Args:
            datos (dict): Diccionario con datos crudos
            
        Returns:
            dict: Diccionario con datos normalizados
        """
        # Limpiar rating (convertir a float)
        if datos.get('rating'):
            try:
                datos['rating'] = datos['rating'].replace(',', '.')
                datos['rating'] = float(datos['rating'])
            except ValueError:
                datos['rating'] = ''
        
        # Limpiar número de reseñas (convertir a int)
        if datos.get('num_resenas'):
            try:
                # Eliminar puntos de miles y convertir
                num_resenas = datos['num_resenas'].replace('.', '').replace(',', '')
                datos['num_resenas'] = int(num_resenas)
            except ValueError:
                datos['num_resenas'] = ''
        
        # Normalizar teléfono
        if datos.get('telefono'):
            # Eliminar caracteres no numéricos excepto + y espacios
            telefono = re.sub(r'[^\d\+\s]', '', datos['telefono'])
            datos['telefono'] = telefono.strip()
        
        return datos
