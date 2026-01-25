# 📞 Cómo Obtener Teléfonos y Sitios Web

## El Problema

Google Maps **NO muestra** teléfonos, sitios web ni emails en la lista de resultados lateral. Solo muestra:
- Nombre
- Rating y reseñas
- Categoría  
- Dirección breve

Para obtener teléfonos y sitios web, **hay que hacer clic en cada lugar individual**.

---

## ⏱️ Impacto en Tiempo

| Modo | Datos | Tiempo por lugar | 100 lugares |
|------|-------|------------------|-------------|
| **Rápido** (actual) | Nombre, rating, dirección | ~0.5 segundos | ~1 minuto |
| **Detallado** (con clic) | + Teléfono, web, email | ~5-8 segundos | ~10 minutos |

**Diferencia:** El modo detallado es 10-15 veces más lento.

---

## ✅ Solución: Modo Detallado (Opcional)

### Opción 1: Modificar config.py (Temporal)

En segment_searcher.py, línea ~160, **descomentar**:

```python
# Después de extraer datos básicos
datos = self.extractor.extraer_datos_basicos(elemento)

# AGREGAR ESTAS LÍNEAS:
if datos['url_google_maps']:
    datos_detallados = self.extractor.extraer_datos_detallados(datos['url_google_maps'])
    datos.update(datos_detallados)
```

---

### Opción 2: Script Separado (Recomendado)

He aquí un script que toma el Excel existente y completa los datos faltantes:

```bash
# Primero extrae rápido (sin teléfonos)
python main.py --rubros "restaurante"

# Luego completa teléfonos (más lento)
python completar_telefonos.py
```

---

## 🚀 Script: completar_telefonos.py

Crea este archivo:

```python
#!/usr/bin/env python3
"""
Completa datos faltantes (teléfono, web, email) haciendo clic en cada lugar
"""
import sys
import pandas as pd
import undetected_chromedriver as uc
from pathlib import Path
import time
import logging

# Importar módulos del scraper
from config import CONFIG, USER_AGENTS
from detail_extractor import DetailExtractor
from utils import setup_logging

def completar_datos():
    # Setup
    logger = setup_logging('logs')
    excel_file = Path('resultados/google_maps_results.xlsx')
    
    if not excel_file.exists():
        print("❌ No se encontró el archivo de resultados")
        return
    
    # Cargar datos
    df = pd.read_excel(excel_file)
    print(f"📊 Cargados {len(df)} lugares")
    
    # Filtrar solo los que NO tienen teléfono
    sin_telefono = df[df['telefono'].isna() | (df['telefono'] == '')]
    print(f"📞 {len(sin_telefono)} lugares sin teléfono")
    
    if len(sin_telefono) == 0:
        print("✅ Todos los lugares ya tienen teléfono!")
        return
    
    # Inicializar navegador
    print("🚀 Inicializando navegador...")
    options = uc.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = uc.Chrome(options=options, use_subprocess=True)
    
    extractor = DetailExtractor(driver)
    
    # Procesar cada lugar
    completados = 0
    for idx, row in sin_telefono.iterrows():
        try:
            url = row['url_google_maps']
            if not url or pd.isna(url):
                continue
            
            print(f"📍 [{completados+1}/{len(sin_telefono)}] {row['nombre'][:40]}...", end='')
            
            # Extraer datos detallados
            datos_detallados = extractor.extraer_datos_detallados(url)
            
            # Actualizar DataFrame
            if datos_detallados['telefono']:
                df.at[idx, 'telefono'] = datos_detallados['telefono']
                print(f" ✅ Tel: {datos_detallados['telefono']}")
            else:
                print(" ⚠️  Sin teléfono")
            
            if datos_detallados['sitio_web']:
                df.at[idx, 'sitio_web'] = datos_detallados['sitio_web']
            
            if datos_detallados['email']:
                df.at[idx, 'email'] = datos_detallados['email']
            
            completados += 1
            
            # Checkpoint cada 10
            if completados % 10 == 0:
                df.to_excel(excel_file, index=False)
                print(f"💾 Checkpoint guardado: {completados} completados")
            
            # Delay entre lugares
            time.sleep(2)
            
        except KeyboardInterrupt:
            print("\n⚠️  Interrumpido por usuario")
            break
        except Exception as e:
            print(f" ❌ Error: {str(e)}")
            continue
    
    # Guardar final
    df.to_excel(excel_file, index=False)
    csv_file = excel_file.with_suffix('.csv')
    df.to_csv(csv_file, index=False, encoding='utf-8-sig')
    
    driver.quit()
    
    # Estadísticas
    con_telefono = df['telefono'].notna().sum()
    print(f"\n✅ Proceso completado")
    print(f"📞 Lugares con teléfono: {con_telefono}/{len(df)} ({con_telefono/len(df)*100:.1f}%)")

if __name__ == "__main__":
    completar_datos()
```

---

## 📝 Uso

### Flujo completo:

```bash
# 1. Extracción rápida (sin teléfonos)
python main.py --rubros "restaurante" "cafetería"
# Resultado: 200 lugares en 5 minutos

# 2. Completar teléfonos (lento)
python completar_telefonos.py
# Resultado: Teléfonos agregados en 20-40 minutos
```

---

## 🎯 Estrategia Recomendada

### Para bases de datos GRANDES (1000+ lugares):

1. **Primera pasada - Rápido:** Extrae todo sin teléfonos
   ```bash
   python main.py --rubros "fabrica" "logistica" "transportes"
   # ~500 lugares en 15-30 minutos
   ```

2. **Filtrar en Excel:** Abre el archivo y filtra solo los lugares que te interesan (ej: rating > 4.0)

3. **Segunda pasada - Detallado:** Completa teléfonos solo de los filtrados
   ```python
   # Modificar completar_telefonos.py para solo procesar rating > 4.0
   sin_telefono = df[(df['telefono'].isna()) & (df['rating'] > 4.0)]
   ```

---

## ⚡ Alternativa: Modo Híbrido

Modifica `config.py` para solo hacer clic cada N lugares:

```python
CONFIG = {
    ...
    'extraer_detalles_cada': 5,  # Solo 1 de cada 5 lugares
}
```

Esto te da una muestra representativa de teléfonos sin hacer el proceso 10x más lento.

---

## 🔍 Por Qué No Están Los Teléfonos

Google Maps tiene dos niveles de información:

### Nivel 1: Lista (Lateral)
- ✅ Nombre
- ✅ Rating
- ✅ Reseñas
- ✅ Categoría
- ❌ Teléfono
- ❌ Sitio web
- ❌ Email

### Nivel 2: Detalle (Click)
- ✅ Todo lo anterior
- ✅ Teléfono
- ✅ Sitio web
- ✅ Email
- ✅ Horarios
- ✅ Fotos

**El script actual** extrae Nivel 1 (rápido).

**Para Nivel 2** necesitas hacer clic en cada lugar (lento).

---

## 💡 Conclusión

- ✅ Script actual es **rápido y eficiente** para obtener listados
- ⚠️ Para teléfonos, necesitas **modo detallado** (10x más lento)
- 🎯 Usa el **flujo de dos pasos**: primero rápido, luego completa

**¿Necesitas teléfonos?**
1. Usa `completar_telefonos.py` después
2. O modifica `segment_searcher.py` para hacer clic en cada lugar

---

**Archivos creados:**
- `completar_telefonos.py` - Script para completar datos
- `COMO_OBTENER_TELEFONOS.md` - Esta guía

**Siguiente paso:**
```bash
python completar_telefonos.py
```
