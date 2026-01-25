# 🚀 Guía de Inicio Rápido

## Instalación en 3 pasos

### 1. Crear entorno virtual y instalar dependencias

```bash
# Opción A: Usando el script automático (recomendado)
bash setup.sh

# Opción B: Manual
python3 -m venv scraper
source scraper/bin/activate  # En Windows: scraper\Scripts\activate
pip install -r requirements.txt
```

### 2. Verificar instalación

```bash
python test.py
```

Si ves "✅ Todas las pruebas pasaron", estás listo para continuar.

### 3. Ejecutar el scraper

```bash
python main.py
```

---

## Personalizar búsqueda

### Opción 1: Por línea de comandos

```bash
# Cambiar ubicación
python main.py --ubicacion "Buenos Aires, Argentina"

# Cambiar rubros
python main.py --rubros "restaurante" "hotel" "gimnasio"

# Cambiar grid size
python main.py --grid-size 3

# Modo headless (sin ventana)
python main.py --headless

# Todo junto
python main.py --ubicacion "Rosario, Argentina" --rubros "fabrica" "logistica" --grid-size 2
```

### Opción 2: Editando config.py

```bash
# Edita el archivo config.py
nano config.py  # o usa tu editor favorito

# Cambia las siguientes líneas:
'ubicacion': "TU_CIUDAD, PAÍS",
'rubros': ["rubro1", "rubro2", "rubro3"],
'grid_size': 2,

# Guarda y ejecuta
python main.py
```

---

## Ejemplos de uso

### Ejemplo 1: Buscar restaurantes en Buenos Aires

```bash
python main.py --ubicacion "Buenos Aires, Argentina" --rubros "restaurante" "bar" "cafetería"
```

### Ejemplo 2: Buscar fábricas en Córdoba (2x2 grid)

```bash
python main.py --ubicacion "Córdoba, Argentina" --rubros "fabrica" "industria" --grid-size 2
```

### Ejemplo 3: Búsqueda exhaustiva con 9 segmentos

```bash
python main.py --ubicacion "Rosario, Santa Fe, Argentina" --rubros "logistica" "transportes" --grid-size 3
```

---

## Monitorear progreso

### Ver logs en tiempo real

```bash
# En otra terminal
tail -f logs/scraper_*.log
```

### Ver resultados parciales

Los resultados se guardan automáticamente cada 20 empresas en:
- `resultados/google_maps_results.xlsx` (archivo principal)
- `backups/backup_TIMESTAMP.xlsx` (backups)

Puedes abrir estos archivos mientras el script está ejecutando.

---

## Pausar y reanudar

### Pausar

Presiona `Ctrl+C` en la terminal donde está ejecutando el scraper.

El script guardará el progreso actual automáticamente.

### Reanudar

Simplemente ejecuta de nuevo:

```bash
python main.py
```

El script detectará el archivo `estado_ejecucion.json` y continuará desde donde se quedó.

### Empezar desde cero

```bash
rm estado_ejecucion.json
rm resultados/*.xlsx
python main.py
```

---

## Solución rápida de problemas

### "ModuleNotFoundError: No module named 'X'"

```bash
source scraper/bin/activate  # Activar entorno virtual
pip install -r requirements.txt
```

### "ChromeDriver not found" o "Chrome not found"

Asegúrate de tener Google Chrome instalado:
- macOS: Descarga desde https://www.google.com/chrome/
- Linux: `sudo apt install google-chrome-stable`

### "No se encontraron resultados"

1. Verifica tu conexión a internet
2. Aumenta los delays en `config.py`
3. Intenta con modo no-headless (`--headless` desactivado)

### El navegador se cierra inmediatamente

Ejecuta sin headless para ver qué está pasando:

```bash
python main.py  # Sin --headless
```

---

## Configuración recomendada por caso de uso

### 🏃 Rápido (pocos resultados, prueba)
```bash
python main.py --ubicacion "Tu Ciudad" --rubros "restaurante" --grid-size 1
```

### 🚶 Normal (balance velocidad/cobertura)
```bash
python main.py --ubicacion "Tu Ciudad" --rubros "rubro1" "rubro2" --grid-size 2
```

### 🐢 Exhaustivo (máxima cobertura)
```bash
python main.py --ubicacion "Tu Ciudad" --rubros "rubro1" "rubro2" "rubro3" --grid-size 4
```

---

## Tips importantes

1. **Empieza pequeño**: Prueba con 1-2 rubros y grid-size 1 primero
2. **Monitorea los logs**: Te dirán exactamente qué está pasando
3. **Sé paciente**: Google Maps puede ser lento, especialmente con muchos resultados
4. **Usa delays apropiados**: No hagas scraping agresivo o Google te bloqueará
5. **Backups automáticos**: Se crean cada 20 empresas, no los borres
6. **Horarios**: Ejecuta preferiblemente en horarios de bajo tráfico

---

## Archivos importantes

- `main.py` - Script principal
- `config.py` - Configuración
- `resultados/google_maps_results.xlsx` - Resultados finales
- `logs/scraper_*.log` - Logs de ejecución
- `estado_ejecucion.json` - Estado para reanudar

---

## Siguiente paso

Una vez que obtengas resultados, puedes:

1. Abrir el Excel y filtrar/ordenar datos
2. Importar a tu CRM
3. Usar para análisis de mercado
4. Exportar a otros formatos

Para más detalles, consulta `README.md`.

---

**¿Todo funcionando? ¡Feliz scraping! 🎉**
