"""
Módulo de gestión de datos
Maneja el almacenamiento, checkpoints y exportación de datos
"""
import logging
import pandas as pd
from pathlib import Path
from datetime import datetime
from utils import guardar_estado, generar_id_unico


class DataManager:
    def __init__(self, config):
        self.config = config
        self.datos = []
        self.df = pd.DataFrame()
        self.empresas_desde_ultimo_checkpoint = 0
        self.total_empresas = 0
        
        # IDs únicos para evitar duplicados
        self.ids_unicos = set()
        
        # Archivo de salida
        self.archivo_excel = Path(config['dir_resultados']) / config['archivo_excel']
        self.archivo_csv = self.archivo_excel.with_suffix('.csv')
        
        # Crear DataFrame vacío con columnas
        self.columnas = [
            'nombre',
            'direccion',
            'ciudad',
            'categoria',
            'rating',
            'num_resenas',
            'telefono',
            'sitio_web',
            'email',
            'url_google_maps',
            'latitud',
            'longitud',
            'rubro_buscado',
            'segmento_id',
            'segmento_centro',
            'fecha_extraccion'
        ]
        
        # 🔥 CARGAR DATOS EXISTENTES SI EXISTEN
        self._cargar_datos_existentes()
    
    def _cargar_datos_existentes(self):
        """
        Carga datos existentes desde archivos previos para NO sobrescribirlos
        """
        try:
            # Intentar cargar desde CSV (más rápido)
            if self.archivo_csv.exists():
                logging.info(f"📂 Cargando datos existentes desde {self.archivo_csv}")
                self.df = pd.read_csv(self.archivo_csv)
                
                # Reconstruir ids_unicos para evitar duplicados
                for _, row in self.df.iterrows():
                    lugar_id = generar_id_unico(
                        row.get('nombre', ''),
                        row.get('direccion', ''),
                        row.get('url_google_maps')
                    )
                    self.ids_unicos.add(lugar_id)
                
                self.total_empresas = len(self.df)
                logging.info(f"✅ {self.total_empresas} empresas cargadas desde archivo previo")
                
            # Si no hay CSV, intentar desde Excel
            elif self.archivo_excel.exists():
                logging.info(f"📂 Cargando datos existentes desde {self.archivo_excel}")
                self.df = pd.read_excel(self.archivo_excel)
                
                # Reconstruir ids_unicos
                for _, row in self.df.iterrows():
                    lugar_id = generar_id_unico(
                        row.get('nombre', ''),
                        row.get('direccion', ''),
                        row.get('url_google_maps')
                    )
                    self.ids_unicos.add(lugar_id)
                
                self.total_empresas = len(self.df)
                logging.info(f"✅ {self.total_empresas} empresas cargadas desde archivo previo")
            
            else:
                logging.info("📝 No hay datos previos - iniciando desde cero")
                
        except Exception as e:
            logging.warning(f"⚠️ No se pudieron cargar datos previos: {str(e)}")
            logging.info("📝 Iniciando con DataFrame vacío")
    
    def agregar_lugares(self, lugares):
        """
        Agrega nuevos lugares al conjunto de datos
        
        Args:
            lugares (list): Lista de diccionarios con datos de lugares
            
        Returns:
            int: Número de lugares agregados (excluyendo duplicados)
        """
        lugares_agregados = 0
        
        for lugar in lugares:
            # Generar ID único usando URL de Google Maps (más confiable)
            lugar_id = generar_id_unico(
                lugar.get('nombre', ''),
                lugar.get('direccion', ''),
                lugar.get('url_google_maps')
            )
            
            if lugar_id not in self.ids_unicos:
                self.ids_unicos.add(lugar_id)
                
                # Agregar fecha de extracción
                lugar['fecha_extraccion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                self.datos.append(lugar)
                lugares_agregados += 1
                self.total_empresas += 1
                self.empresas_desde_ultimo_checkpoint += 1
        
        if lugares_agregados > 0:
            logging.info(f"📊 {lugares_agregados} lugares agregados (Total: {self.total_empresas})")
            
            # Verificar si es momento de hacer checkpoint
            if self.empresas_desde_ultimo_checkpoint >= self.config['checkpoint_cada']:
                self.guardar_checkpoint()
        
        return lugares_agregados
    
    def crear_dataframe(self):
        """
        Crea o actualiza el DataFrame de pandas con los datos NUEVOS
        y los COMBINA con los datos existentes
        """
        if self.datos:
            # Crear DataFrame con datos NUEVOS
            df_nuevos = pd.DataFrame(self.datos)
            
            # Asegurar que todas las columnas existan
            for columna in self.columnas:
                if columna not in df_nuevos.columns:
                    df_nuevos[columna] = ''
            
            # COMBINAR con datos existentes
            if not self.df.empty:
                # Concatenar datos previos + nuevos
                self.df = pd.concat([self.df, df_nuevos], ignore_index=True)
            else:
                # Si no había datos previos, usar solo los nuevos
                self.df = df_nuevos
            
            # Reordenar columnas
            columnas_existentes = [col for col in self.columnas if col in self.df.columns]
            self.df = self.df[columnas_existentes]
            
            # Limpiar lista de datos nuevos (ya están en el DataFrame)
            self.datos = []
    
    def guardar_checkpoint(self):
        """
        Guarda un checkpoint de los datos actuales
        SIEMPRE agrega a datos existentes, NUNCA sobrescribe
        """
        try:
            # Si hay datos nuevos, agregarlos al DataFrame
            if self.datos:
                self.crear_dataframe()
            
            # VERIFICACIÓN: Si el DataFrame está vacío pero hay archivo previo, cargarlo
            if self.df.empty and (self.archivo_csv.exists() or self.archivo_excel.exists()):
                logging.warning("⚠️ DataFrame vacío detectado - recargando datos previos")
                self._cargar_datos_existentes()
            
            # Si aún está vacío, no guardar
            if self.df.empty:
                logging.warning("No hay datos para guardar en checkpoint")
                return
            
            # 🔒 GUARDAR de forma segura (primero backup, luego guardar)
            # Crear backup temporal si existe el archivo
            if self.archivo_csv.exists():
                import shutil
                backup_temp = self.archivo_csv.with_suffix('.csv.backup_temp')
                shutil.copy2(self.archivo_csv, backup_temp)
                logging.info(f"🔒 Backup temporal creado: {backup_temp}")
            
            # Guardar archivos principales
            self.df.to_excel(self.archivo_excel, index=False, engine='openpyxl')
            self.df.to_csv(self.archivo_csv, index=False, encoding='utf-8-sig')
            
            logging.info(f"💾 Checkpoint guardado: {len(self.df)} empresas TOTALES")
            
            # Eliminar backup temporal si todo salió bien
            backup_temp = self.archivo_csv.with_suffix('.csv.backup_temp')
            if backup_temp.exists():
                backup_temp.unlink()
            
            # Resetear contador
            self.empresas_desde_ultimo_checkpoint = 0
            
        except Exception as e:
            logging.error(f"❌ Error guardando checkpoint: {str(e)}")
            # Intentar restaurar backup si existe
            backup_temp = self.archivo_csv.with_suffix('.csv.backup_temp')
            if backup_temp.exists():
                import shutil
                shutil.copy2(backup_temp, self.archivo_csv)
                logging.info("🔄 Backup temporal restaurado")
            raise
    
    def guardar_final(self):
        """
        Guarda la versión final de los datos
        SIEMPRE agrega a datos existentes, NUNCA sobrescribe
        """
        try:
            # Si hay datos nuevos, agregarlos al DataFrame
            if self.datos:
                self.crear_dataframe()
            
            # VERIFICACIÓN: Si el DataFrame está vacío pero hay archivo previo, cargarlo
            if self.df.empty and (self.archivo_csv.exists() or self.archivo_excel.exists()):
                logging.warning("⚠️ DataFrame vacío detectado - recargando datos previos")
                self._cargar_datos_existentes()
            
            # Si aún está vacío, no guardar
            if self.df.empty:
                logging.warning("No hay datos para guardar")
                return
            
            # 🔒 GUARDAR de forma segura (primero backup, luego guardar)
            if self.archivo_csv.exists():
                import shutil
                backup_temp = self.archivo_csv.with_suffix('.csv.backup_temp')
                shutil.copy2(self.archivo_csv, backup_temp)
                logging.info(f"🔒 Backup temporal creado antes de guardar final")
            
            # Guardar archivo final en Excel Y CSV
            self.df.to_excel(self.archivo_excel, index=False, engine='openpyxl')
            logging.info(f"✅ Archivo Excel guardado: {self.archivo_excel}")
            
            self.df.to_csv(self.archivo_csv, index=False, encoding='utf-8-sig')
            logging.info(f"✅ Archivo CSV guardado: {self.archivo_csv}")
            
            logging.info(f"   📊 Total de lugares: {len(self.df)}")
            
            # Eliminar backup temporal si todo salió bien
            backup_temp = self.archivo_csv.with_suffix('.csv.backup_temp')
            if backup_temp.exists():
                backup_temp.unlink()
            
            # Estadísticas
            self.mostrar_estadisticas()
            
        except Exception as e:
            logging.error(f"❌ Error guardando archivo final: {str(e)}")
            # Intentar restaurar backup si existe
            backup_temp = self.archivo_csv.with_suffix('.csv.backup_temp')
            if backup_temp.exists():
                import shutil
                shutil.copy2(backup_temp, self.archivo_csv)
                logging.info("🔄 Backup temporal restaurado")
            raise
    
    def mostrar_estadisticas(self):
        """
        Muestra estadísticas de los datos recolectados
        """
        if self.df.empty:
            logging.info("No hay datos para estadísticas")
            return
        
        logging.info("\n" + "="*60)
        logging.info("📊 ESTADÍSTICAS FINALES")
        logging.info("="*60)
        
        # Total de lugares
        logging.info(f"Total de lugares únicos: {len(self.df)}")
        
        # Por ciudad
        if 'ciudad' in self.df.columns:
            ciudades = self.df['ciudad'].value_counts()
            logging.info("\nLugares por ciudad:")
            for ciudad, count in ciudades.items():
                logging.info(f"  - {ciudad}: {count}")
        
        # Por rubro
        if 'rubro_buscado' in self.df.columns:
            rubros = self.df['rubro_buscado'].value_counts()
            logging.info("\nTop 10 rubros:")
            for rubro, count in list(rubros.items())[:10]:
                logging.info(f"  - {rubro}: {count}")
        
        # Por segmento
        if 'segmento_id' in self.df.columns:
            segmentos = self.df['segmento_id'].value_counts()
            logging.info(f"\nLugares por segmento:")
            for segmento, count in segmentos.items():
                logging.info(f"  - Segmento {segmento}: {count}")
        
        # Lugares con teléfono
        if 'telefono' in self.df.columns:
            con_telefono = self.df['telefono'].notna().sum()
            porcentaje = (con_telefono / len(self.df) * 100) if len(self.df) > 0 else 0
            logging.info(f"\nLugares con teléfono: {con_telefono} ({porcentaje:.1f}%)")
        
        # Lugares con sitio web
        if 'sitio_web' in self.df.columns:
            con_web = self.df['sitio_web'].notna().sum()
            porcentaje = (con_web / len(self.df) * 100) if len(self.df) > 0 else 0
            logging.info(f"Lugares con sitio web: {con_web} ({porcentaje:.1f}%)")
        
        # Rating promedio
        if 'rating' in self.df.columns:
            ratings_validos = pd.to_numeric(self.df['rating'], errors='coerce').dropna()
            if len(ratings_validos) > 0:
                rating_promedio = ratings_validos.mean()
                logging.info(f"Rating promedio: {rating_promedio:.2f}")
        
        logging.info("="*60 + "\n")
    
    def cargar_datos_previos(self):
        """
        Carga datos de una ejecución anterior si existen
        """
        try:
            if self.archivo_excel.exists():
                self.df = pd.read_excel(self.archivo_excel, engine='openpyxl')
                self.datos = self.df.to_dict('records')
                
                # Reconstruir IDs únicos
                for dato in self.datos:
                    lugar_id = generar_id_unico(
                        dato.get('nombre', ''),
                        dato.get('direccion', ''),
                        dato.get('url_google_maps')
                    )
                    self.ids_unicos.add(lugar_id)
                
                self.total_empresas = len(self.datos)
                logging.info(f"✅ Datos previos cargados: {self.total_empresas} lugares")
                
                return True
        except Exception as e:
            logging.warning(f"No se pudieron cargar datos previos: {str(e)}")
        
        return False
