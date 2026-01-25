# Cambios Realizados - Versión 1.1

## Fecha: 24 de Enero 2026

## Problemas Reportados y Soluciones

### 1. ❌ No extrae teléfono ni email
**Problema:** Los campos de teléfono y email aparecen vacíos en los resultados.

**Causa:** Los selectores CSS/XPath no capturaban estos datos de Google Maps.

**Solución Aplicada:**
- ✅ Agregados nuevos selectores para teléfono en `config.py`:
  - `'telefono_lista'`: Busca por aria-label
  - `'telefono_lista_alt'`: Busca patrones de teléfono en el HTML
- ✅ Implementada función `extraer_telefono_de_html_texto()` en `detail_extractor.py` que busca patrones de teléfonos argentinos e internacionales
- ✅ Patrones de búsqueda:
  - +54 351 1234567 (formato internacional)
  - 0351 1234567 (formato nacional)
  - (351) 1234567 (formato con paréntesis)

**Estado:** ⚠️ PARCIALMENTE RESUELTO
- Google Maps NO muestra teléfonos en la lista de resultados por defecto
- Para obtener teléfonos, se necesita hacer clic en cada lugar (mucho más lento)
- Recomendación: Implementar extracción detallada si los teléfonos son críticos

---

### 2. ❌ Scroll automático no funciona
**Problema:** El scraper solo extraía ~16 lugares cuando debería extraer cientos.

**Causa:** El algoritmo de scroll no detectaba correctamente cuándo se cargaban más elementos.

**Solución Aplicada:**
- ✅ Mejorado algoritmo de scroll en `segment_searcher.py`
- ✅ Cambio de estrategia: en vez de comparar altura del contenedor, ahora cuenta elementos antes y después del scroll
- ✅ Scroll más natural usando `scrollTo()` en vez de `scrollTop`
- ✅ Delays apropiados después de cada scroll

**Resultado:**
- ✅ Ahora extrae 98 lugares (vs 16 anteriormente) 
- ✅ Funciona correctamente hasta agotar resultados

---

### 3. ❌ Extrae duplicados desde otras partes de la ciudad
**Problema:** El scraper vuelve a empezar y extrae lugares repetidos.

**Causa:** `grid_size = 2` dividía la ciudad en 4 cuadrantes, buscando en cada uno.

**Solución Aplicada:**
- ✅ Cambiado `grid_size` de 2 a 1 en `config.py`
- ✅ Agregados comentarios explicativos sobre qué hace grid_size
- ✅ Ajustado `zoom_level` de 13 a 11 para cubrir toda la ciudad de una vez

**Explicación:**
```python
grid_size = 1  # 1x1 = 1 segmento (NO divide el área)
grid_size = 2  # 2x2 = 4 cuadrantes (divide en 4 zonas)
grid_size = 3  # 3x3 = 9 cuadrantes (divide en 9 zonas)
```

**Resultado:**
- ✅ Ya no extrae duplicados de diferentes zonas
- ✅ Una sola pasada por toda la ciudad

---

### 4. ❌ Genera múltiples archivos de backup
**Problema:** Quería UN SOLO archivo Excel y uno CSV, no múltiples backups.

**Solución Aplicada:**
- ✅ Modificado `data_manager.py` para eliminar backups automáticos con timestamp
- ✅ Ahora guarda SOLO:
  - `resultados/google_maps_results.xlsx` (archivo principal Excel)
  - `resultados/google_maps_results.csv` (archivo principal CSV)
- ✅ Ambos archivos se actualizan en cada checkpoint
- ✅ El CSV es más ligero para bases de datos grandes

**Resultado:**
- ✅ Un solo archivo Excel
- ✅ Un solo archivo CSV
- ✅ Ambos se actualizan sincronizados

---

## Mejoras Adicionales

### 5. ✅ Compatibilidad con undetected-chromedriver
- Simplificada inicialización del navegador
- Eliminadas opciones experimentales problemáticas
- Ahora funciona con la última versión de Chrome

### 6. ✅ Mejor manejo de errores
- Más información de debug en logs
- Detecta cuándo no hay más resultados para cargar

---

## Configuración Recomendada

```python
CONFIG = {
    'ubicacion': "Tu Ciudad, País",
    'rubros': ["rubro1", "rubro2"],
    
    # NO dividir el área (grid_size = 1)
    'grid_size': 1,  # 1 segmento = toda la ciudad
    'zoom_level': 11,  # Zoom para ciudad completa
    
    # Delays apropiados
    'delays': {
        'entre_rubros': (4, 8),
        'despues_scroll': (2, 4),
    },
    
    # Checkpoints cada 20 empresas
    'checkpoint_cada': 20,
}
```

---

## Limitaciones Conocidas

### Teléfono y Email
- ⚠️ **Google Maps NO muestra teléfonos en la lista de resultados**
- Para obtenerlos, necesitas hacer clic en cada lugar individualmente
- Esto haría el scraping 10-20 veces más lento
- **Opción futura:** Implementar `extraer_datos_detallados()` con flag opcional

### Scroll Infinito
- ✅ Funciona bien hasta ~100-500 resultados por rubro
- Google Maps limita los resultados mostrados
- Para obtener MÁS resultados, usa `grid_size > 1` (divide en zonas)

### Datos Disponibles en Lista
Los siguientes datos SÍ se extraen de la lista:
- ✅ Nombre
- ✅ Rating (puntuación)
- ✅ Número de reseñas
- ✅ Categoría
- ✅ Dirección breve
- ✅ URL de Google Maps
- ✅ Coordenadas GPS
- ❌ Teléfono (NO disponible en lista)
- ❌ Email (NO disponible en lista)
- ❌ Sitio web (NO disponible en lista)

---

## Próximos Pasos Sugeridos

1. **Para obtener teléfonos:**
   - Implementar modo "detallado" que hace clic en cada lugar
   - Usar flag: `python main.py --modo-detallado`
   - Estimar: 5-10 segundos por lugar

2. **Para más resultados:**
   - Usar `grid_size = 3` o `grid_size = 4`
   - Esto divide en 9 o 16 zonas
   - Cuidado con duplicados (ya hay deduplicación)

3. **Para múltiples ciudades:**
   - Ejecutar varias veces con diferentes ubicaciones
   - Los archivos se sobrescriben, guardar con nombres diferentes

---

## Comandos Útiles

```bash
# Ejecutar con configuración por defecto
python main.py

# Ejecutar con rubros específicos (1 segmento)
python main.py --rubros "restaurante" "cafetería"

# Ver resultados
head -20 resultados/google_maps_results.csv

# Analizar estadísticas
python analizar_resultados.py
```

---

## Versión

- **v1.0**: Release inicial
- **v1.1**: Arreglos de scroll, segmentación y archivos únicos

**Última actualización:** 24/01/2026
