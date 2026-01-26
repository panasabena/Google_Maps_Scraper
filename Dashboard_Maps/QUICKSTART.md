# 🚀 Inicio Rápido - Dashboard de Scraping Argentina

## Instalación en 3 Pasos

### 1️⃣ Ejecutar Script de Instalación

```bash
cd /Users/panasabena/Scraper_Maps/Dashboard_Maps
./install.sh
```

El script automáticamente:
- ✅ Crea el entorno virtual "Dossier"
- ✅ Instala todas las dependencias
- ✅ Verifica los archivos de datos
- ✅ Configura los directorios

### 2️⃣ Activar Entorno Virtual (si no lo hizo el script)

```bash
source Dossier/bin/activate
```

### 3️⃣ Iniciar el Dashboard

```bash
python app.py
```

### 4️⃣ Abrir en el Navegador

```
http://localhost:8050/
```

---

## Instalación Manual (Alternativa)

Si prefieres instalar manualmente:

```bash
# 1. Crear entorno virtual
python3 -m venv Dossier

# 2. Activar entorno virtual
source Dossier/bin/activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Ejecutar dashboard
python app.py
```

---

## Solución de Problemas Comunes

### Error: "No module named 'dash'"
```bash
source Dossier/bin/activate
pip install -r requirements.txt
```

### Error: "No such file or directory" (CSV o JSON)
Verifica las rutas en `config.py`:
```python
FILE_PATHS = {
    'csv_data': '/Users/panasabena/Scraper_Maps/resultados/google_maps_results.csv',
    'estado_json': '/Users/panasabena/Scraper_Maps/estado_ejecucion.json',
    # ...
}
```

### Puerto 8050 ocupado
Cambia el puerto en `config.py`:
```python
DASHBOARD_CONFIG = {
    'port': 8051,  # Cambiar a otro puerto
    # ...
}
```

### Dashboard sin datos
Verifica que los archivos existan:
```bash
ls -la /Users/panasabena/Scraper_Maps/resultados/google_maps_results.csv
ls -la /Users/panasabena/Scraper_Maps/estado_ejecucion.json
```

---

## Características del Dashboard

### 📊 Resumen General
- Total de empresas extraídas
- Progreso general del scraping
- Métricas de calidad de datos
- Indicadores visuales

### 🗺️ Mapa Interactivo
- Ubicaciones con estado de procesamiento
- Mapa de calor de densidad
- Scatter maps por provincia/categoría

### 📈 Estadísticas
- Top 10 provincias
- Top 15 categorías
- Timeline de extracciones
- Distribución de ratings
- Filtros avanzados

### ⚙️ Progreso
- Progreso por provincia
- Estado de ubicaciones
- Rubros completados

### 📄 Datos
- Tabla interactiva de empresas
- Búsqueda avanzada
- Exportación a CSV

---

## Actualización de Datos

El dashboard se actualiza automáticamente cada 5 minutos. También puedes:
- Hacer clic en "🔄 Actualizar Ahora"
- Modificar el intervalo en `config.py`

---

## Acceso desde Otra Computadora

Si quieres acceder desde otra computadora en la misma red:

1. Encuentra tu IP local:
```bash
ifconfig | grep "inet " | grep -v 127.0.0.1
```

2. Abre en el navegador:
```
http://<tu-ip>:8050/
```

---

## Detener el Dashboard

Presiona `Ctrl + C` en la terminal donde está corriendo.

---

## Desactivar Entorno Virtual

```bash
deactivate
```

---

## Próximos Pasos

1. ✅ Personaliza colores en `assets/css/style.css`
2. ✅ Ajusta configuración en `config.py`
3. ✅ Agrega más ubicaciones o rubros según necesites
4. ✅ Revisa el `README.md` completo para funciones avanzadas

---

**¿Necesitas ayuda?** Revisa el archivo `README.md` completo o los logs en `logs/dashboard.log`
