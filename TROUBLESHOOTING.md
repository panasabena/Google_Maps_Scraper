# Troubleshooting Guide - Google Maps Scraper

## Problemas Comunes y Soluciones

### 1. Error de instalación de dependencias

#### Problema: `error: command 'gcc' failed`

**Causa**: Faltan herramientas de compilación necesarias para Shapely.

**Solución macOS**:
```bash
# Instalar Homebrew si no lo tienes
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar geos
brew install geos

# Reinstalar Shapely
pip uninstall shapely
pip install shapely
```

**Solución Linux (Ubuntu/Debian)**:
```bash
sudo apt-get update
sudo apt-get install build-essential libgeos-dev
pip install shapely
```

#### Problema: `ModuleNotFoundError: No module named 'X'`

**Solución**:
```bash
# Asegúrate de estar en el entorno virtual
source scraper/bin/activate

# Reinstalar todas las dependencias
pip install -r requirements.txt
```

---

### 2. Problemas con el navegador

#### Problema: `selenium.common.exceptions.SessionNotCreatedException`

**Causa**: Incompatibilidad entre versión de Chrome y ChromeDriver.

**Solución**:
```bash
# Actualizar Chrome a la última versión
# macOS: Chrome se actualiza automáticamente
# Linux:
sudo apt update
sudo apt upgrade google-chrome-stable

# Reinstalar undetected-chromedriver
pip uninstall undetected-chromedriver
pip install undetected-chromedriver
```

#### Problema: El navegador se cierra inmediatamente

**Solución 1**: Verificar que Chrome esté instalado
```bash
# macOS
open -a "Google Chrome"

# Linux
which google-chrome
```

**Solución 2**: Desactivar headless mode
```python
# En config.py
'headless': False
```

**Solución 3**: Verificar permisos
```bash
# macOS: Permitir Chrome en Preferencias del Sistema > Seguridad y privacidad
```

---

### 3. Problemas de scraping

#### Problema: No se encuentran elementos en la página

**Causa**: Google cambió los selectores HTML.

**Solución temporal**:
```bash
# Ejecutar sin headless para ver qué está pasando
python main.py --headless false

# Verificar si hay mensajes de error en los logs
cat logs/scraper_*.log | grep ERROR
```

**Solución permanente**: Actualizar selectores en `config.py`
1. Inspeccionar la página de Google Maps manualmente
2. Encontrar los nuevos selectores CSS/XPath
3. Actualizar `SELECTORS` en `config.py`

#### Problema: "Consent screen" no se maneja

**Solución**:
```python
# En segment_searcher.py, agregar más selectores de consentimiento
SELECTORS['consent_button_extra'] = "//button[contains(text(), 'Rechazar')]"
```

#### Problema: Se extraen 0 resultados

**Causas posibles**:
1. Ubicación no encontrada
2. Rubro mal escrito
3. Selectores desactualizados
4. Bloqueado por Google

**Diagnóstico**:
```bash
# Ver logs detallados
tail -f logs/scraper_*.log

# Probar geolocalización
python geolocator.py

# Ejecutar tests
python test.py
```

---

### 4. Problemas de conectividad

#### Problema: `requests.exceptions.ConnectionError`

**Causa**: Sin conexión a internet o firewall bloqueando.

**Solución**:
```bash
# Verificar conexión
ping google.com

# Verificar que puedes acceder a Nominatim
curl https://nominatim.openstreetmap.org/search?q=Cordoba&format=json

# Si estás detrás de un proxy, configurarlo
export HTTP_PROXY=http://proxy:port
export HTTPS_PROXY=http://proxy:port
```

#### Problema: `TimeoutException` constante

**Causa**: Red lenta o delays muy cortos.

**Solución**: Aumentar delays en `config.py`
```python
'delays': {
    'entre_segmentos': (15, 25),
    'entre_rubros': (8, 15),
    'despues_scroll': (4, 6),
    'carga_inicial': (5, 10)
}
```

---

### 5. Problemas de bloqueo

#### Problema: Google muestra CAPTCHA

**Causa**: Detección de scraping.

**Soluciones**:

1. **Pausar y esperar**:
```bash
# Pausar el scraper (Ctrl+C)
# Esperar 1-2 horas
# Reiniciar con delays más largos
```

2. **Aumentar delays**:
```python
# En config.py
'delays': {
    'entre_segmentos': (30, 60),
    'entre_rubros': (15, 30),
    'despues_scroll': (5, 10),
    'carga_inicial': (10, 15)
}
```

3. **Cambiar IP**:
```bash
# Reiniciar router
# O usar VPN
```

4. **Usar modo no-headless**:
```python
'headless': False
```

#### Problema: IP bloqueada temporalmente

**Síntomas**: No se cargan páginas, errores 429.

**Solución**:
- Esperar 24 horas
- Usar otra red (datos móviles, VPN)
- Reducir agresividad del scraping

---

### 6. Problemas de datos

#### Problema: Muchos duplicados

**Causa**: Segmentos se solapan.

**Solución**: Reducir `grid_size` o aumentar `zoom_level`
```python
'grid_size': 2,  # En vez de 4
'zoom_level': 14,  # En vez de 12
```

#### Problema: Faltan datos (teléfono, email, etc.)

**Causa**: Google Maps no muestra todos los datos en la lista.

**Solución**: Implementar extracción detallada (hacer clic en cada lugar)
```python
# En segment_searcher.py, descomentar:
# datos_detallados = self.extractor.extraer_datos_detallados(datos['url_google_maps'])
```

**Nota**: Esto hace el scraping MUCHO más lento.

#### Problema: Excel no se genera

**Causa**: Error en pandas o openpyxl.

**Diagnóstico**:
```python
# Verificar instalación
python -c "import pandas; import openpyxl; print('OK')"
```

**Solución**:
```bash
pip install --upgrade pandas openpyxl
```

---

### 7. Problemas de rendimiento

#### Problema: El scraper es muy lento

**Optimizaciones**:

1. **Reducir delays** (con cuidado):
```python
'delays': {
    'entre_segmentos': (5, 10),
    'entre_rubros': (2, 5),
    'despues_scroll': (1, 2),
}
```

2. **Reducir scrolls máximos**:
```python
'max_scrolls_por_pagina': 10,  # En vez de 20
```

3. **Limitar rubros**:
```python
'rubros': ["fabrica", "logistica"],  # Solo los más importantes
```

#### Problema: Alto uso de memoria

**Causa**: Muchos datos en memoria.

**Solución**: Reducir `checkpoint_cada`
```python
'checkpoint_cada': 10,  # En vez de 20
```

---

### 8. Problemas con el entorno virtual

#### Problema: `command not found: source`

**Causa**: Usando shell incorrecto (fish, csh).

**Solución**:
```bash
# Usar bash
bash
source scraper/bin/activate
```

#### Problema: Entorno virtual no se activa

**Solución**: Recrear entorno
```bash
rm -rf scraper/
python3 -m venv scraper
source scraper/bin/activate
pip install -r requirements.txt
```

---

### 9. Problemas específicos de macOS

#### Problema: "Python no está instalado" (pero sí lo está)

**Causa**: Usando Python de Xcode en vez de Python 3.

**Solución**:
```bash
# Instalar Python 3 con Homebrew
brew install python3

# Usar python3 explícitamente
python3 -m venv scraper
```

#### Problema: Permiso denegado al ejecutar Chrome

**Solución**:
1. Ir a Preferencias del Sistema > Seguridad y Privacidad
2. Permitir aplicaciones de desarrolladores identificados
3. Permitir Chrome explícitamente

---

### 10. Otros problemas

#### Problema: Estado corrupto

**Síntomas**: Errores extraños, comportamiento inconsistente.

**Solución**: Resetear estado
```bash
python utils_cli.py limpiar
# O manualmente:
rm estado_ejecucion.json cookies.pkl
```

#### Problema: Logs muy grandes

**Solución**: Limpiar logs antiguos
```bash
# Eliminar logs de hace más de 7 días
find logs/ -name "*.log" -mtime +7 -delete
```

---

## Obtener ayuda adicional

### Logs útiles para debugging

```bash
# Ver últimas 50 líneas de logs
tail -50 logs/scraper_*.log

# Buscar errores
grep ERROR logs/scraper_*.log

# Ver warnings
grep WARNING logs/scraper_*.log
```

### Modo verbose

Para más información de debugging, edita `utils.py`:
```python
logging.basicConfig(
    level=logging.DEBUG,  # En vez de INFO
    ...
)
```

### Información del sistema

```bash
# Versión de Python
python3 --version

# Versiones de paquetes
pip list

# Información del SO
uname -a  # Linux/macOS
```

---

## Prevención de problemas

### Checklist antes de ejecutar

- [ ] Entorno virtual activado
- [ ] Dependencias instaladas
- [ ] Chrome instalado y actualizado
- [ ] Conexión a internet estable
- [ ] Ubicación válida en config.py
- [ ] Delays apropiados configurados
- [ ] Suficiente espacio en disco

### Checklist durante ejecución

- [ ] Monitorear logs regularmente
- [ ] Verificar checkpoints se están guardando
- [ ] Verificar que no hay CAPTCHAs
- [ ] Verificar uso de memoria/CPU

### Buenas prácticas

1. **Empieza pequeño**: Prueba con 1 rubro y grid_size=1
2. **Incrementa gradualmente**: Si funciona, aumenta rubros/segmentos
3. **Monitorea constantemente**: Revisa logs cada 15-30 minutos
4. **No seas agresivo**: Usa delays generosos
5. **Backups**: Los checkpoints son tu amigo
6. **Horarios**: Ejecuta en horas de bajo tráfico

---

Si ninguna solución funciona, revisa:
1. Logs completos en `logs/`
2. Estado en `estado_ejecucion.json`
3. Resultados parciales en `backups/`
