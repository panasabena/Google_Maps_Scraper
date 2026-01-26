# 🗺️ Dashboard de Monitoreo de Scraping Argentina

Dashboard interactivo en Python para visualizar el progreso y resultados del scraping de Google Maps en Argentina. Desarrollado con Dash, Plotly y Bootstrap.

![Dashboard Preview](assets/images/dashboard-preview.png)

## 📋 Descripción

Este dashboard permite monitorear en tiempo real:
- ✅ Progreso del scraping en 28 ubicaciones de Argentina
- 📊 Estadísticas de más de 100K+ empresas extraídas
- 🗺️ Mapas interactivos con densidad de empresas
- 📈 Análisis de calidad de datos
- 🎯 Filtros avanzados por provincia, rubro y más

## 🚀 Características Principales

### 1. Resumen General
- **Cards de métricas**: Total de empresas, progreso, provincias, calidad de datos
- **Gráficos de progreso**: Gauge y donut chart con porcentaje completado
- **Indicadores de calidad**: Empresas con email, teléfono, sitio web, rating

### 2. Mapas Interactivos
- **Mapa de ubicaciones**: 28 ciudades con estado de procesamiento (completo/parcial/pendiente)
- **Mapa de densidad**: Heatmap de empresas extraídas
- **Scatter maps**: Empresas coloreadas por provincia o categoría

### 3. Estadísticas Detalladas
- **Top 10 provincias** con más empresas
- **Top 15 categorías** más frecuentes
- **Timeline**: Empresas extraídas por día (diario y acumulado)
- **Distribución de ratings**: Histograma de ratings
- **Filtros dinámicos**: Por provincia, rubro, rating, calidad de datos

### 4. Progreso de Scraping
- **Progreso por provincia**: Gráfico de barras horizontal
- **Tabla de ubicaciones**: Estado detallado de cada ubicación
- **Combinaciones**: 28 ubicaciones × 196 rubros = 5,488 combinaciones

### 5. Tabla de Datos
- **Búsqueda**: Por nombre, ciudad o categoría
- **Paginación**: 50 filas por página
- **Exportación**: Descarga a CSV
- **Filtros nativos**: En cada columna

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Paso 1: Crear Entorno Virtual

```bash
# Navegar al directorio del proyecto
cd /Users/panasabena/Scraper_Maps/Dashboard_Maps

# Crear entorno virtual llamado "Dossier"
python3 -m venv Dossier

# Activar el entorno virtual
# En macOS/Linux:
source Dossier/bin/activate

# En Windows:
# Dossier\Scripts\activate
```

### Paso 2: Instalar Dependencias

```bash
# Con el entorno virtual activado
pip install -r requirements.txt
```

### Paso 3: Verificar Rutas de Archivos

Edita el archivo `config.py` y verifica que las rutas apunten a tus archivos:

```python
FILE_PATHS = {
    'csv_data': '/Users/panasabena/Scraper_Maps/resultados/google_maps_results.csv',
    'estado_json': '/Users/panasabena/Scraper_Maps/estado_ejecucion.json',
    'geojson_provincias': '/Users/panasabena/Scraper_Maps/Dashboard_Maps/data/geo/argentina_provincias.geojson',
    'geojson_departamentos': '/Users/panasabena/Scraper_Maps/Dashboard_Maps/data/geo/argentina_departamentos.geojson',
    'logs': '/Users/panasabena/Scraper_Maps/Dashboard_Maps/logs/dashboard.log'
}
```

## 🎮 Uso

### Iniciar el Dashboard

```bash
# Con el entorno virtual activado
python app.py
```

Verás algo como esto:

```
============================================================
🚀 Dashboard de Monitoreo de Scraping Argentina
============================================================
📊 Empresas cargadas: 125,430
📍 Ubicaciones configuradas: 28
🏷️  Rubros configurados: 196
🌐 Servidor iniciando en http://localhost:8050/
============================================================
```

### Acceder al Dashboard

Abre tu navegador y ve a:
```
http://localhost:8050/
```

O desde otra computadora en la misma red:
```
http://<tu-ip-local>:8050/
```

### Actualización Automática

El dashboard se actualiza automáticamente cada 5 minutos (configurable). También puedes hacer clic en el botón **"🔄 Actualizar Ahora"** para refrescar manualmente.

## 📁 Estructura del Proyecto

```
Dashboard_Maps/
├── app.py                      # Aplicación principal
├── config.py                   # Configuración (ubicaciones, rubros)
├── requirements.txt            # Dependencias
├── README.md                   # Este archivo
│
├── src/                        # Módulos de código
│   ├── data_loader.py         # Carga y procesamiento de datos
│   ├── statistics_calculator.py # Cálculo de estadísticas
│   ├── progress_tracker.py    # Seguimiento de progreso
│   ├── map_generator.py       # Generación de mapas
│   └── utils.py               # Utilidades (opcional)
│
├── data/                       # Datos y archivos geográficos
│   └── geo/
│       ├── argentina_provincias.geojson
│       └── argentina_departamentos.geojson
│
├── assets/                     # Recursos estáticos
│   ├── css/
│   │   └── style.css          # Estilos personalizados
│   └── images/
│       └── dashboard-preview.png
│
├── logs/                       # Logs de la aplicación
│   └── dashboard.log
│
└── Dossier/                    # Entorno virtual (no incluir en git)
```

## ⚙️ Configuración

### Cambiar Puerto del Servidor

Edita `config.py`:

```python
DASHBOARD_CONFIG = {
    'port': 8050,  # Cambia a otro puerto si lo deseas
    'debug': True,  # False para producción
    # ...
}
```

### Ajustar Intervalo de Actualización

```python
DASHBOARD_CONFIG = {
    'update_interval': 300,  # segundos (300 = 5 minutos)
    # ...
}
```

### Personalizar Colores

```python
DASHBOARD_CONFIG = {
    'status_colors': {
        'completed': '#28a745',  # Verde
        'partial': '#ffc107',    # Amarillo
        'pending': '#dc3545'     # Rojo
    },
    # ...
}
```

## 🎨 Personalización de Estilos

Los estilos se encuentran en `assets/css/style.css`. Dash carga automáticamente cualquier archivo CSS en la carpeta `assets/`.

### Cambiar Colores del Header

```css
.dashboard-header {
    background: linear-gradient(135deg, #TU-COLOR-1 0%, #TU-COLOR-2 100%);
    /* ... */
}
```

### Modo Oscuro

Para activar el modo oscuro, agrega la clase `dark-mode` al body (requiere JavaScript personalizado).

## 📊 Datos de Entrada

### CSV de Empresas (`google_maps_results.csv`)

Columnas esperadas:
- `nombre`: Nombre de la empresa
- `direccion`: Dirección
- `ciudad`: Ciudad
- `categoria`: Categoría del negocio
- `rating`: Rating (1-5)
- `num_resenas`: Número de reseñas
- `telefono`: Teléfono
- `sitio_web`: Sitio web
- `email`: Email
- `url_google_maps`: URL de Google Maps
- `latitud`: Latitud
- `longitud`: Longitud
- `rubro_buscado`: Rubro usado en la búsqueda
- `segmento_id`: ID del segmento
- `segmento_centro`: Centro del segmento
- `fecha_extraccion`: Fecha de extracción

### JSON de Estado (`estado_ejecucion.json`)

Estructura esperada:

```json
{
    "ubicaciones_completadas": {
        "buenos_aires_argentina": {
            "nombre": "Buenos Aires, Argentina",
            "rubros_completados": ["fabrica", "logistica", "..."],
            "ultima_actualizacion": "2024-01-24T15:30:00"
        },
        "cordoba_argentina": {
            "nombre": "Córdoba, Argentina",
            "rubros_completados": ["restaurante", "hotel", "..."]
        }
        // ... más ubicaciones
    }
}
```

## 🗺️ Archivos GeoJSON

Para los mapas coropléticos, necesitas archivos GeoJSON de Argentina:

### Descargar GeoJSON

Puedes obtener archivos GeoJSON de Argentina desde:

1. **Natural Earth**: https://www.naturalearthdata.com/
2. **INDEC**: https://www.indec.gob.ar/
3. **GitHub geoJSON**: https://github.com/data/geojson

### Estructura esperada del GeoJSON

```json
{
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "nombre": "Buenos Aires",
                "id": "02"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [...]
            }
        }
        // ... más provincias
    ]
}
```

## 🔧 Solución de Problemas

### Error: "No such file or directory"

**Causa**: Las rutas en `config.py` no son correctas.

**Solución**: Verifica que los archivos existan en las rutas especificadas:

```bash
ls -la /Users/panasabena/Scraper_Maps/resultados/google_maps_results.csv
ls -la /Users/panasabena/Scraper_Maps/estado_ejecucion.json
```

### Error: "Module not found"

**Causa**: Dependencias no instaladas o entorno virtual no activado.

**Solución**:

```bash
# Activar entorno virtual
source Dossier/bin/activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### El dashboard no muestra datos

**Causa**: Archivos CSV o JSON vacíos o mal formateados.

**Solución**:

1. Verifica que el CSV tenga datos:
   ```bash
   wc -l /Users/panasabena/Scraper_Maps/resultados/google_maps_results.csv
   ```

2. Verifica el formato del JSON:
   ```bash
   python -m json.tool /Users/panasabena/Scraper_Maps/estado_ejecucion.json
   ```

### Puerto 8050 ya en uso

**Causa**: Otra aplicación está usando ese puerto.

**Solución**: Cambia el puerto en `config.py` o mata el proceso:

```bash
# Encontrar el proceso
lsof -i :8050

# Matar el proceso (reemplaza PID con el número del proceso)
kill -9 PID
```

## 📈 Rendimiento

### Optimizaciones Implementadas

1. **Caching**: Los datos se cachean en memoria y solo se recargan si los archivos cambian
2. **Chunks**: Los archivos CSV grandes se leen en chunks
3. **Muestreo**: Los mapas con muchos puntos usan muestreo (max 10,000 puntos)
4. **Tipos optimizados**: Pandas usa tipos de datos optimizados para reducir memoria

### Recomendaciones

- **CSV > 500MB**: Considera usar una base de datos (SQLite, PostgreSQL)
- **Muchos usuarios**: Despliega con Gunicorn en producción
- **Actualizaciones frecuentes**: Reduce el intervalo de actualización

## 🚀 Despliegue en Producción

### Opción 1: Servidor Local con Gunicorn

```bash
# Instalar Gunicorn (ya está en requirements.txt)
pip install gunicorn

# Ejecutar con Gunicorn
gunicorn app:server -b 0.0.0.0:8050 --workers 4
```

### Opción 2: Docker

Crea un `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8050

CMD ["python", "app.py"]
```

Construir y ejecutar:

```bash
docker build -t dashboard-scraping .
docker run -p 8050:8050 -v /ruta/a/datos:/datos dashboard-scraping
```

### Opción 3: Cloud (Render, Heroku, AWS)

El dashboard puede desplegarse fácilmente en plataformas cloud. Consulta la documentación de cada plataforma para Dash apps.

## 📝 Logs

Los logs se guardan en `logs/dashboard.log`:

```bash
# Ver logs en tiempo real
tail -f logs/dashboard.log
```

## 🤝 Contribuciones

Si deseas agregar funcionalidades:

1. Crea módulos adicionales en `src/`
2. Importa en `app.py`
3. Agrega callbacks para interactividad
4. Actualiza los estilos en `assets/css/style.css`

## 📧 Soporte

Para problemas o preguntas, revisa:
1. Esta documentación
2. Los logs en `logs/dashboard.log`
3. La consola donde ejecutaste `python app.py`

## 📜 Licencia

Este proyecto es de uso interno. Todos los derechos reservados.

## 🎯 Roadmap Futuro

- [ ] Exportar reportes PDF
- [ ] Envío de notificaciones por email
- [ ] Integración con API de scraping para control remoto
- [ ] Dashboard multi-usuario con autenticación
- [ ] Análisis predictivo con Machine Learning
- [ ] Comparativas temporales (mes a mes)
- [ ] Alertas automáticas por caídas de calidad

---

**Desarrollado con ❤️ para el monitoreo eficiente del scraping de Google Maps en Argentina**

*Última actualización: Enero 2026*
