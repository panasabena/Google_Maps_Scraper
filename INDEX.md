# 📋 Índice de Documentación - Google Maps Scraper

Bienvenido al sistema de scraping de Google Maps con estrategia estilo Apify.

## 📖 Documentación Disponible

### 🚀 Para Empezar

1. **[README.md](README.md)**
   - Descripción general del proyecto
   - Características principales
   - Instalación completa
   - Uso básico y avanzado
   - FAQ y consideraciones

2. **[QUICKSTART.md](QUICKSTART.md)**
   - Guía de inicio rápido
   - Instalación en 3 pasos
   - Ejemplos de uso inmediato
   - Configuraciones recomendadas
   - Tips importantes

### 🏗️ Documentación Técnica

3. **[ARQUITECTURA.md](ARQUITECTURA.md)**
   - Diseño del sistema
   - Componentes y módulos
   - Flujo de datos
   - Diagramas de arquitectura
   - Métricas de rendimiento

### 🔧 Soporte y Mantenimiento

4. **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)**
   - Problemas comunes y soluciones
   - Debugging paso a paso
   - Errores de instalación
   - Problemas de navegador
   - Guía de recuperación

### 📝 Configuración

5. **[config.py](config.py)**
   - Configuración principal del scraper
   - Parámetros de búsqueda
   - Selectores CSS/XPath
   - Delays y límites

6. **[config_example.py](config_example.py)**
   - Ejemplos de configuraciones
   - Casos de uso específicos
   - Configuraciones optimizadas

## 🛠️ Scripts Disponibles

### Scripts Principales

| Script | Propósito | Uso |
|--------|-----------|-----|
| `main.py` | Ejecutar el scraper | `python main.py [opciones]` |
| `test.py` | Verificar instalación | `python test.py` |
| `setup.sh` | Instalación automatizada | `bash setup.sh` |

### Scripts de Utilidades

| Script | Propósito | Uso |
|--------|-----------|-----|
| `utils_cli.py` | Utilidades CLI | `python utils_cli.py [comando]` |
| `analizar_resultados.py` | Análisis de datos | `python analizar_resultados.py` |
| `geolocator.py` | Test de geolocalización | `python geolocator.py` |

## 📚 Guías por Rol

### Para Usuarios Nuevos
1. Empieza con [QUICKSTART.md](QUICKSTART.md)
2. Ejecuta `bash setup.sh`
3. Personaliza `config.py` según tu necesidad
4. Ejecuta `python main.py`
5. Si hay problemas, consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

### Para Usuarios Avanzados
1. Lee [README.md](README.md) para entender todas las opciones
2. Revisa [config_example.py](config_example.py) para configuraciones optimizadas
3. Usa argumentos de línea de comandos para control fino
4. Consulta [ARQUITECTURA.md](ARQUITECTURA.md) para optimizaciones

### Para Desarrolladores
1. Estudia [ARQUITECTURA.md](ARQUITECTURA.md) para entender el diseño
2. Revisa el código fuente de cada módulo
3. Usa `test.py` para verificar cambios
4. Consulta selectores en `config.py` si Google actualiza su HTML

## 🎯 Casos de Uso Comunes

### 1. Extracción Rápida (una ciudad, pocos rubros)
```bash
python main.py --ubicacion "Tu Ciudad" --rubros "restaurante" --grid-size 1
```
**Documentación:** QUICKSTART.md > Ejemplos de uso

### 2. Extracción Exhaustiva (múltiples rubros, área grande)
```bash
python main.py --ubicacion "Tu Ciudad" --rubros "fabrica" "logistica" --grid-size 3
```
**Documentación:** README.md > Uso con parámetros personalizados

### 3. Análisis de Resultados
```bash
python analizar_resultados.py
```
**Documentación:** README.md > Salida de Datos

### 4. Recuperación después de Error
```bash
# Simplemente ejecuta de nuevo, el estado se recupera automáticamente
python main.py
```
**Documentación:** README.md > Recuperación de Errores

### 5. Filtrar Resultados por Rubro
```bash
python utils_cli.py filtrar "fabrica"
```
**Documentación:** README.md > Utilidades CLI

## 🔍 Búsqueda Rápida

### "¿Cómo instalo el scraper?"
→ [QUICKSTART.md](QUICKSTART.md) - Sección "Instalación en 3 pasos"

### "¿Por qué no funciona?"
→ [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Diagnóstico completo

### "¿Cómo cambio la ciudad/rubros?"
→ [QUICKSTART.md](QUICKSTART.md) - Sección "Personalizar búsqueda"

### "¿Cuánto tiempo tarda?"
→ [ARQUITECTURA.md](ARQUITECTURA.md) - Sección "Métricas de Rendimiento"

### "¿Cómo funciona internamente?"
→ [ARQUITECTURA.md](ARQUITECTURA.md) - Visión completa

### "Error: ChromeDriver not found"
→ [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Sección "Problemas con el navegador"

### "¿Puedo pausar y reanudar?"
→ [README.md](README.md) - Sección "Recuperación de Errores"

### "¿Qué datos extrae exactamente?"
→ [README.md](README.md) - Sección "Datos Extraídos"

## 📊 Estructura de Archivos

```
Scraper_Maps/
├── 📄 README.md                    # Documentación principal
├── 📄 QUICKSTART.md                # Guía rápida
├── 📄 ARQUITECTURA.md              # Diseño técnico
├── 📄 TROUBLESHOOTING.md           # Solución de problemas
├── 📄 INDEX.md                     # Este archivo
│
├── 🐍 main.py                      # Script principal
├── 🐍 config.py                    # Configuración
├── 🐍 geolocator.py               # Geolocalización
├── 🐍 segment_searcher.py         # Búsqueda
├── 🐍 detail_extractor.py         # Extracción
├── 🐍 data_manager.py             # Datos
├── 🐍 utils.py                    # Utilidades
│
├── 🔧 test.py                     # Tests
├── 🔧 utils_cli.py                # Utilidades CLI
├── 🔧 analizar_resultados.py     # Análisis
├── 🔧 setup.sh                    # Instalación
│
├── 📦 requirements.txt            # Dependencias
├── 🔒 .gitignore                  # Git ignore
│
├── 📁 resultados/                 # Archivos Excel/CSV
├── 📁 backups/                    # Backups automáticos
└── 📁 logs/                       # Logs de ejecución
```

## 🆘 Obtener Ayuda

### Orden Recomendado:

1. **Consulta la documentación** apropiada según tu problema
2. **Revisa los logs** en `logs/scraper_*.log`
3. **Ejecuta los tests** con `python test.py`
4. **Verifica el estado** con `python utils_cli.py estado`
5. **Busca en TROUBLESHOOTING** tu error específico

## 🔄 Actualizaciones

### Versión Actual: 1.0

**Última actualización:** Enero 2024

### Changelog:

- v1.0 (Enero 2024): Release inicial
  - Geolocalización con Nominatim
  - Búsqueda por segmentos
  - Scroll infinito
  - Checkpoints automáticos
  - Anti-detección básica
  - Exportación Excel/CSV

## 📞 Contacto y Contribuciones

Este es un proyecto educacional. Las contribuciones son bienvenidas:

- Mejoras en selectores (cuando Google cambia)
- Optimizaciones de rendimiento
- Nuevas features
- Corrección de bugs
- Mejoras en documentación

## 🎓 Recursos Adicionales

### Externos:

- [Documentación de Selenium](https://selenium-python.readthedocs.io/)
- [Documentación de Pandas](https://pandas.pydata.org/docs/)
- [Nominatim API](https://nominatim.org/release-docs/latest/api/Overview/)
- [Shapely Documentation](https://shapely.readthedocs.io/)

### Internos:

- Revisa los comentarios en el código fuente
- Cada módulo tiene docstrings detallados
- Los ejemplos en `config_example.py` son educativos

---

**¿Listo para empezar?**

👉 Ve a [QUICKSTART.md](QUICKSTART.md) y comienza en 3 pasos.

**¿Tienes problemas?**

👉 Consulta [TROUBLESHOOTING.md](TROUBLESHOOTING.md) para soluciones.

**¿Quieres entender cómo funciona?**

👉 Lee [ARQUITECTURA.md](ARQUITECTURA.md) para detalles técnicos.

---

**Happy Scraping! 🗺️**
