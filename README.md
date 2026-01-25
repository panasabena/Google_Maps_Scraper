# 🗺️ Google Maps Scraper - Estrategia Apify

Script profesional de web scraping para Google Maps que replica la estrategia utilizada por Apify.

## 🎯 Características

- **Geolocalización inteligente**: Convierte ubicaciones textuales en polígonos usando Nominatim
- **División geográfica**: Divide el área en segmentos para cobertura completa
- **Búsqueda multi-rubro**: Busca múltiples categorías de negocios
- **Scroll infinito**: Maneja la paginación automática de Google Maps
- **Anti-detección**: Usa undetected-chromedriver y comportamiento humano
- **Checkpoints automáticos**: Guarda progreso cada 20 empresas
- **Logs detallados**: Sistema de logging estilo Apify
- **Recuperación de errores**: Puede retomar desde donde se quedó

## 📊 Datos Extraídos

Para cada lugar/negocio extrae:

- Nombre del lugar
- Dirección completa
- Categoría/rubro
- Rating/puntuación
- Número de reseñas
- Teléfono (cuando está disponible)
- Sitio web (cuando está disponible)
- Email (cuando está disponible)
- Coordenadas (latitud, longitud)
- URL de Google Maps

## 🛠️ Instalación

### 1. Crear entorno virtual

```bash
python3 -m venv scraper
source scraper/bin/activate  # En Windows: scraper\Scripts\activate
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Verificar instalación

```bash
python -c "import selenium; import undetected_chromedriver; print('OK')"
```

## 🚀 Uso

### Uso básico

```bash
python main.py
```

Esto usará la configuración por defecto en `config.py`.

### Uso con parámetros personalizados

```bash
# Cambiar ubicación
python main.py --ubicacion "Buenos Aires, Argentina"

# Cambiar rubros
python main.py --rubros fabrica logistica transportes

# Cambiar tamaño de grid
python main.py --grid-size 3

# Modo headless
python main.py --headless

# Combinación
python main.py --ubicacion "Rosario, Argentina" --rubros "restaurante" "hotel" --grid-size 2
```

## ⚙️ Configuración

Edita `config.py` para personalizar:

```python
CONFIG = {
    'ubicacion': "Córdoba, Argentina",
    'rubros': ["fabrica", "logistica", "transportes"],
    'grid_size': 2,  # 2x2 = 4 segmentos
    'zoom_level': 13,
    'checkpoint_cada': 20,  # empresas
    'delays': {
        'entre_segmentos': (8, 15),
        'entre_rubros': (4, 8),
        'despues_scroll': (2, 4)
    }
}
```

## 📁 Estructura del Proyecto

```
Scraper_Maps/
├── main.py                      # Script principal
├── config.py                    # Configuración
├── geolocator.py               # Geolocalización y segmentación
├── segment_searcher.py         # Búsqueda por segmento
├── detail_extractor.py         # Extracción de detalles
├── data_manager.py             # Gestión de datos y checkpoints
├── utils.py                    # Utilidades comunes
├── requirements.txt            # Dependencias Python
├── README.md                   # Este archivo
├── resultados/                 # Archivos Excel generados
├── backups/                    # Backups automáticos
├── logs/                       # Logs de ejecución
├── estado_ejecucion.json      # Estado para recuperación
└── cookies.pkl                # Cookies de sesión
```

## 📈 Proceso de Ejecución

1. **Geolocalización**: Convierte la ubicación en polígono
2. **Segmentación**: Divide el área en cuadrícula
3. **Búsqueda**: Para cada segmento y rubro:
   - Navega a Google Maps
   - Maneja scroll infinito
   - Extrae datos de lugares
4. **Almacenamiento**: Guarda en Excel con checkpoints

## 🔧 Ejemplo de Logs

```
2024-01-24T10:30:00 INFO  📡 Geolocalizando: Córdoba, Argentina
2024-01-24T10:30:02 INFO  ✅ Ubicación encontrada
2024-01-24T10:30:02 INFO  📐 Dividiendo área en cuadrícula de 2x2
2024-01-24T10:30:02 INFO  ✅ Creados 4 segmentos
2024-01-24T10:30:05 INFO  🔍 Buscando 'fabrica' en segmento 0
2024-01-24T10:30:45 INFO  🔍 [fabrica][-31.4201|-64.1888][SCROLL: 8]: Search page scraped: 42 unique, 5 duplicate, 47 seen, 8 paginations, 2 outOfLocation.
2024-01-24T10:30:45 INFO  📊 42 lugares agregados (Total: 42)
```

## ⚠️ Consideraciones Importantes

### Límites de Google Maps

- Google puede detectar y bloquear scraping excesivo
- Usa delays apropiados entre solicitudes
- No ejecutes el script 24/7
- Considera usar la API oficial para uso comercial

### Uso Responsable

- Este script es para fines educativos
- Respeta los términos de servicio de Google
- No sobrecargues los servidores de Google
- Usa los datos de manera ética

### Anti-Detección

El script incluye:
- User-Agent rotation
- Delays aleatorios
- undetected-chromedriver
- Comportamiento similar al humano

Aún así, Google puede detectarlo. Para uso en producción considera:
- Proxies rotativos
- Distribución de IPs
- API oficial de Google Places

## 🐛 Solución de Problemas

### Error: "ChromeDriver not found"

```bash
# Instalar webdriver-manager
pip install webdriver-manager
```

### Error: "Shapely no funciona"

```bash
# En macOS
brew install geos

# En Ubuntu/Debian
sudo apt-get install libgeos-dev

# Reinstalar Shapely
pip uninstall shapely
pip install shapely --no-binary shapely
```

### El navegador se cierra inmediatamente

- Verifica que Chrome esté instalado
- Usa modo no-headless para debugging
- Revisa los logs en `logs/`

### No se encuentran resultados

- Verifica la ubicación sea válida
- Revisa los selectores en `config.py` (Google puede cambiarlos)
- Aumenta los delays en la configuración
- Verifica tu conexión a internet

## 📊 Salida de Datos

Los datos se guardan en:

- **Excel principal**: `resultados/google_maps_results.xlsx`
- **CSV**: `resultados/google_maps_results.csv`
- **Backups**: `backups/backup_YYYYMMDD_HHMMSS.xlsx`

Columnas del Excel:
- nombre
- direccion
- categoria
- rating
- num_resenas
- telefono
- sitio_web
- url_google_maps
- latitud
- longitud
- rubro_buscado
- segmento_id
- fecha_extraccion

## 🔄 Recuperación de Errores

Si el script se interrumpe:

1. El estado se guarda en `estado_ejecucion.json`
2. Los datos parciales están en checkpoints
3. Al reiniciar, continuará desde donde se quedó

Para empezar desde cero:

```bash
rm estado_ejecucion.json
rm resultados/*.xlsx
```

## 📝 Licencia

Este proyecto es para fines educativos. Usa bajo tu propia responsabilidad.

## 🤝 Contribuciones

Mejoras sugeridas:
- Implementar extracción desde `APP_INITIALIZATION_STATE`
- Agregar soporte para proxies
- Implementar cola de tareas distribuida
- Mejorar detección de fin de resultados

## 📞 Soporte

Para problemas o preguntas:
1. Revisa los logs en `logs/`
2. Verifica la configuración en `config.py`
3. Consulta la sección de solución de problemas

---

**⚡ Happy Scraping!**
