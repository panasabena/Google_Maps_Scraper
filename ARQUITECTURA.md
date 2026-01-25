# 🏗️ Arquitectura del Sistema - Google Maps Scraper

## Visión General

Este documento describe la arquitectura técnica completa del scraper de Google Maps, diseñado para replicar la estrategia utilizada por Apify.

---

## 📐 Diagrama de Componentes

```
┌─────────────────────────────────────────────────────────────────┐
│                         MAIN.PY (Orquestador)                    │
│  - Inicializa componentes                                        │
│  - Gestiona el flujo principal                                   │
│  - Maneja errores y recuperación                                 │
└───────────────┬─────────────────────────────────────────────────┘
                │
    ┌───────────┴───────────┐
    │                       │
    ▼                       ▼
┌─────────────┐     ┌──────────────┐
│ GEOLOCATOR  │     │   CONFIG     │
│             │     │              │
│ - Nominatim │     │ - Settings   │
│ - Polygons  │     │ - Selectors  │
│ - Segments  │     │ - Delays     │
└──────┬──────┘     └──────────────┘
       │
       ▼
┌─────────────────────────────────┐
│   SEGMENT_SEARCHER              │
│                                 │
│ - URL Builder                   │
│ - Page Navigation               │
│ - Scroll Handler                │
│ - Results Extraction            │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│   DETAIL_EXTRACTOR              │
│                                 │
│ - Basic Data Extraction         │
│ - Detailed Data Extraction      │
│ - Data Normalization            │
└──────────┬──────────────────────┘
           │
           ▼
┌─────────────────────────────────┐
│   DATA_MANAGER                  │
│                                 │
│ - Data Storage                  │
│ - Checkpoint Management         │
│ - Excel Export                  │
│ - Statistics                    │
└─────────────────────────────────┘
```

---

## 🔧 Módulos Principales

### 1. main.py - Orquestador Principal

**Responsabilidades:**
- Inicialización del sistema
- Gestión del flujo de ejecución
- Manejo de errores globales
- Coordinación entre módulos

**Flujo de ejecución:**
```python
1. Cargar configuración
2. Inicializar driver de Selenium
3. Geolocalización de la ubicación
4. División en segmentos geográficos
5. Para cada segmento:
   a. Para cada rubro:
      - Buscar en Google Maps
      - Extraer resultados
      - Guardar datos
   b. Checkpoint si es necesario
6. Guardar resultados finales
7. Cerrar driver
```

**Clase Principal:**
```python
class GoogleMapsScraper:
    - config: dict
    - driver: WebDriver
    - geolocator: Geolocator
    - data_manager: DataManager
    - estado: dict
    
    Methods:
    - inicializar_driver()
    - ejecutar()
```

---

### 2. geolocator.py - Geolocalización y Segmentación

**Responsabilidades:**
- Convertir ubicación textual en polígono
- Dividir área en segmentos
- Cálculo de coordenadas centrales

**Clase Principal:**
```python
class Geolocator:
    - base_url: str (Nominatim API)
    - headers: dict
    
    Methods:
    - obtener_poligono_ubicacion(ubicacion) -> (polygon, bbox)
    - dividir_poligono_en_segmentos(polygon, grid_size) -> [segmentos]
    - punto_esta_en_segmento(lat, lng, segmento) -> bool
```

**Dependencias Externas:**
- Nominatim API (OpenStreetMap)
- Shapely (manipulación geométrica)

**Formato de Segmento:**
```python
{
    'id': 0,
    'bounds': (min_x, min_y, max_x, max_y),
    'centro': (lat, lng),
    'box': Polygon,
    'area': float
}
```

---

### 3. segment_searcher.py - Búsqueda por Segmento

**Responsabilidades:**
- Construcción de URLs de búsqueda
- Navegación de páginas
- Manejo de scroll infinito
- Extracción de lista de resultados

**Clase Principal:**
```python
class SegmentSearcher:
    - driver: WebDriver
    - config: dict
    - wait: WebDriverWait
    - extractor: DetailExtractor
    
    Methods:
    - construir_url_busqueda(rubro, segmento) -> str
    - manejar_consentimiento() -> bool
    - detectar_fin_resultados() -> bool
    - hacer_scroll(elemento_feed) -> bool
    - extraer_resultados_pagina(rubro, segmento) -> [lugares]
    - buscar_en_segmento(rubro, segmento) -> [lugares]
```

**Algoritmo de Scroll Infinito:**
```
1. Localizar feed de resultados
2. Mientras no se alcance el límite:
   a. Extraer elementos visibles
   b. Filtrar duplicados (por ID único)
   c. Hacer scroll hacia abajo
   d. Esperar carga de nuevos elementos
   e. Si no hay nuevos elementos: break
3. Retornar lista de lugares únicos
```

---

### 4. detail_extractor.py - Extracción de Detalles

**Responsabilidades:**
- Extracción de datos básicos (desde lista)
- Extracción de datos detallados (haciendo clic)
- Normalización y limpieza de datos

**Clase Principal:**
```python
class DetailExtractor:
    - driver: WebDriver
    - wait: WebDriverWait
    
    Methods:
    - extraer_datos_basicos(elemento) -> dict
    - extraer_datos_detallados(url_lugar) -> dict
    - extraer_telefono_de_html(elemento) -> str
    - normalizar_datos(datos) -> dict
```

**Estructura de Datos Extraídos:**
```python
{
    'nombre': str,
    'direccion': str,
    'categoria': str,
    'rating': float,
    'num_resenas': int,
    'telefono': str,
    'sitio_web': str,
    'email': str,
    'url_google_maps': str,
    'latitud': str,
    'longitud': str,
    'rubro_buscado': str,
    'segmento_id': int,
    'fecha_extraccion': str
}
```

---

### 5. data_manager.py - Gestión de Datos

**Responsabilidades:**
- Almacenamiento en memoria
- Control de duplicados
- Sistema de checkpoints
- Exportación a Excel/CSV
- Estadísticas

**Clase Principal:**
```python
class DataManager:
    - config: dict
    - datos: list
    - df: DataFrame
    - ids_unicos: set
    - total_empresas: int
    
    Methods:
    - agregar_lugares(lugares) -> int
    - crear_dataframe()
    - guardar_checkpoint()
    - guardar_final()
    - mostrar_estadisticas()
    - cargar_datos_previos()
```

**Sistema de Checkpoints:**
- Checkpoint automático cada N empresas (configurable)
- Backup timestamped en cada checkpoint
- Estado de ejecución en JSON
- Capacidad de recuperación ante fallos

---

### 6. config.py - Configuración Central

**Contenido:**
- Parámetros de búsqueda (ubicación, rubros)
- Configuración de segmentación (grid_size, zoom)
- Límites y controles
- Delays entre acciones
- Configuración anti-detección
- Selectores CSS/XPath

**Selectores Principales:**
```python
SELECTORS = {
    'resultados_feed': "div[role='feed']",
    'lugar_elemento': "//div[@role='feed']//div[contains(@class, 'Nv2PK')]",
    'nombre': ".//div[contains(@class, 'qBF1Pd')]",
    'direccion_breve': ".//div[contains(@class, 'W4Efsd')]//span[last()]",
    'rating': ".//span[contains(@class, 'MW4etd')]",
    'consent_button': "//button[.//span[contains(text(), 'Aceptar')]]"
}
```

---

### 7. utils.py - Utilidades Comunes

**Funciones Principales:**
```python
- setup_logging(log_dir) -> Logger
- crear_directorios(config)
- delay_aleatorio(rango) -> float
- guardar_cookies(driver, archivo)
- cargar_cookies(driver, archivo)
- guardar_estado(estado, archivo)
- cargar_estado(archivo) -> dict
- ejecutar_con_reintentos(func, max_reintentos, descripcion)
- limpiar_texto(texto) -> str
- generar_id_unico(nombre, direccion) -> int
- formato_log_apify(...) -> str
```

---

## 🔄 Flujo de Datos

```
1. INPUT (Usuario)
   - Ubicación: "Córdoba, Argentina"
   - Rubros: ["fabrica", "logistica"]
   
2. GEOLOCALIZACIÓN
   - Nominatim API → Polígono
   - División → 4 segmentos
   
3. BÚSQUEDA
   Para cada segmento (4):
     Para cada rubro (2):
       - URL: https://www.google.com/maps/search/{rubro}/@{lat},{lng},{zoom}z
       - Scroll infinito → ~100-500 resultados
       
4. EXTRACCIÓN
   Para cada resultado:
     - Datos básicos desde HTML
     - Normalización
     - Filtrado de duplicados
     
5. ALMACENAMIENTO
   - Memoria (lista)
   - Checkpoint cada 20 empresas → Excel
   - DataFrame final → Excel + CSV
   
6. OUTPUT
   - Excel: resultados/google_maps_results.xlsx
   - Backups: backups/backup_TIMESTAMP.xlsx
   - Logs: logs/scraper_TIMESTAMP.log
   - Estado: estado_ejecucion.json
```

---

## 🛡️ Estrategia Anti-Detección

### Técnicas Implementadas:

1. **undetected-chromedriver**
   - Evita flags de detección de Selenium
   - Oculta propiedades de webdriver

2. **Delays Aleatorios**
   - Entre 2-4s después de scroll
   - Entre 4-8s entre rubros
   - Entre 8-15s entre segmentos

3. **Comportamiento Humano**
   - Scroll progresivo (no instantáneo)
   - Tiempos de "lectura" variables
   - Manejo de pantallas de consentimiento

4. **User-Agent Rotation**
   - Rotación cada N solicitudes
   - Múltiples user-agents preconfigurados

5. **Cookies Persistentes**
   - Guardado de sesión
   - Reutilización en siguiente ejecución

### Límites de Seguridad:

- Max scrolls por página: 20 (configurable)
- Max empresas por día: 2000 (configurable)
- Delays mínimos: 2 segundos
- No ejecución headless por defecto

---

## 💾 Sistema de Persistencia

### Archivos Generados:

1. **estado_ejecucion.json**
   ```json
   {
     "rubros_completados": [],
     "segmentos_completados": {
       "seg_0": {"rubros": [...], "completado": true}
     },
     "empresas_extraidas": 150,
     "ultimo_checkpoint": "2024-01-24T10:30:00",
     "fecha_inicio": "2024-01-24T09:00:00"
   }
   ```

2. **cookies.pkl**
   - Cookies de sesión en formato pickle
   - Reutilización para evitar re-autenticación

3. **resultados/google_maps_results.xlsx**
   - Archivo principal de resultados
   - Columnas: nombre, dirección, teléfono, etc.

4. **backups/backup_TIMESTAMP.xlsx**
   - Backups automáticos cada checkpoint
   - Formato: backup_20240124_103000.xlsx

5. **logs/scraper_TIMESTAMP.log**
   - Logs detallados de ejecución
   - Formato estilo Apify

---

## 🔍 Sistema de Logging

### Niveles de Log:

- **INFO**: Operaciones normales, progreso
- **WARNING**: Advertencias no críticas
- **ERROR**: Errores que no detienen ejecución
- **DEBUG**: Información detallada para debugging

### Formato:

```
2024-01-24T10:30:00 INFO  🔍 [fabrica][-31.4201|-64.1888][SCROLL: 8]: Search page scraped: 42 unique, 5 duplicate, 47 seen, 8 paginations, 2 outOfLocation.
```

### Salidas:

- Console (stdout)
- Archivo log con timestamp
- Codificación UTF-8

---

## 🧪 Testing y Validación

### Scripts de Test:

1. **test.py**
   - Test de dependencias
   - Test de módulos propios
   - Test de geolocalización
   - Test de directorios

2. **utils_cli.py**
   - Ver estado
   - Analizar resultados
   - Filtrar por rubro
   - Limpiar proyecto

3. **analizar_resultados.py**
   - Reporte completo
   - Estadísticas detalladas
   - Exportación por rubro
   - Búsqueda por criterios

---

## 🚀 Optimizaciones Posibles

### Nivel 1 (Implementadas):
- [x] Detección de duplicados por hash
- [x] Checkpoints automáticos
- [x] Recuperación ante errores
- [x] Logs estructurados

### Nivel 2 (Futuras):
- [ ] Extracción de APP_INITIALIZATION_STATE
- [ ] Paralelización por segmentos
- [ ] Sistema de proxies rotativos
- [ ] Cache de resultados de geolocalización
- [ ] Rate limiting adaptativo

### Nivel 3 (Avanzadas):
- [ ] Distribución con Celery/RQ
- [ ] Base de datos (PostgreSQL)
- [ ] API REST para control
- [ ] Dashboard web en tiempo real
- [ ] Machine learning para detección de bloqueos

---

## 📊 Métricas de Rendimiento

### Tiempo Estimado:

```
Por lugar: ~1-2 segundos
Por página (20 lugares): ~40-80 segundos
Por rubro (100 lugares): ~5-10 minutos
Por segmento (3 rubros): ~15-30 minutos
Total (4 segmentos, 9 rubros): ~2-4 horas
```

### Recursos:

- **Memoria**: ~200-500 MB
- **CPU**: ~10-30% (un core)
- **Red**: ~1-5 MB/minuto
- **Disco**: ~10-50 MB (resultados + logs)

---

## 🔐 Seguridad y Privacidad

### Datos Sensibles:

- No se almacenan contraseñas
- No se interceptan comunicaciones
- Solo se extraen datos públicos de Google Maps

### Archivos a no versionar (.gitignore):

- cookies.pkl (sesión personal)
- estado_ejecucion.json (estado local)
- resultados/ (datos extraídos)
- backups/ (copias)
- logs/ (información de ejecución)

---

## 📚 Dependencias Externas

### Python Packages:

1. **selenium** (4.16.0)
   - WebDriver automation
   
2. **undetected-chromedriver** (3.5.4)
   - Anti-detección
   
3. **beautifulsoup4** (4.12.2)
   - HTML parsing (backup)
   
4. **pandas** (2.1.4)
   - Manipulación de datos
   
5. **openpyxl** (3.1.2)
   - Exportación Excel
   
6. **shapely** (2.0.2)
   - Geometría geográfica
   
7. **requests** (2.31.0)
   - HTTP requests (Nominatim)

### APIs Externas:

1. **Nominatim** (OpenStreetMap)
   - Geolocalización
   - Rate limit: 1 req/segundo
   - No requiere API key

2. **Google Maps**
   - Scraping (no API oficial)
   - Rate limits variables
   - Posibles bloqueos

---

## 🎯 Casos de Uso

### 1. Prospección Comercial
- Extraer negocios de un rubro específico
- Obtener datos de contacto
- Segmentar por zona geográfica

### 2. Análisis de Mercado
- Densidad de competidores
- Distribución geográfica
- Análisis de ratings

### 3. Validación de Datos
- Verificar existencia de negocios
- Actualizar bases de datos
- Completar información faltante

### 4. Investigación Académica
- Estudios urbanos
- Análisis de servicios
- Mapeo de infraestructura

---

## 📝 Mantenimiento

### Tareas Regulares:

1. **Actualizar selectores** (cuando Google cambia HTML)
2. **Limpiar logs antiguos** (> 30 días)
3. **Verificar dependencias** (pip list --outdated)
4. **Backup de resultados importantes**
5. **Monitorear tasa de éxito**

### Señales de que algo necesita actualización:

- [ ] 0 resultados extraídos
- [ ] Muchos errores de "NoSuchElementException"
- [ ] Pantallas de consentimiento no manejadas
- [ ] Chrome no se inicia

---

## 🤝 Contribuciones Futuras

### Áreas de Mejora:

1. **Extracción más eficiente**
   - Parsear JSON interno de Google Maps
   - Evitar hacer clic en cada lugar

2. **Mejor detección de fin**
   - Análisis de cursor interno
   - Detección de mensajes en múltiples idiomas

3. **Soporte multi-idioma**
   - Selectores para diferentes locales
   - Normalización de datos internacionales

4. **Visualización**
   - Mapa de calor de resultados
   - Gráficos de distribución
   - Dashboard interactivo

---

Este documento describe la arquitectura completa del sistema al momento de la versión 1.0.
