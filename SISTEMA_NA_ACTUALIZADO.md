# ✅ SISTEMA N/A IMPLEMENTADO

## 📋 Cambios Realizados

### Modificado: `detail_extractor.py`

#### 1. Método `extraer_datos_basicos()` (vista de lista)

**Teléfono:**
```python
# Intenta encontrar teléfono en múltiples lugares
telefono_encontrado = False
try:
    # Buscar en aria-label
    telefono_elem = elemento.find_element(...)
    datos['telefono'] = ...
    telefono_encontrado = True
except:
    # Buscar en HTML con regex
    telefono = self.extraer_telefono_de_html_texto(html)
    if telefono:
        datos['telefono'] = telefono
        telefono_encontrado = True

# Si no encontró nada → N/A
if not telefono_encontrado or not datos['telefono']:
    datos['telefono'] = 'N/A'
```

**Sitio Web:**
```python
if not datos.get('sitio_web'):
    datos['sitio_web'] = 'N/A'
```

**Email:**
```python
# Siempre N/A en vista de lista (nunca está disponible ahí)
datos['email'] = 'N/A'
```

---

#### 2. Método `extraer_datos_detallados()` (cuando hace clic)

**Teléfono:**
```python
try:
    telefono_elem = self.wait.until(...)
    datos_detallados['telefono'] = limpiar_texto(telefono_elem.text)
except TimeoutException:
    datos_detallados['telefono'] = 'N/A'  # ← Agregado
```

**Sitio Web:**
```python
try:
    web_elem = self.driver.find_element(...)
    datos_detallados['sitio_web'] = web_elem.get_attribute('href')
except NoSuchElementException:
    datos_detallados['sitio_web'] = 'N/A'  # ← Agregado
```

**Email:**
```python
try:
    email_elem = self.driver.find_element(...)
    if 'mailto:' in email_href:
        datos_detallados['email'] = email_href.replace('mailto:', '')
    else:
        datos_detallados['email'] = 'N/A'  # ← Agregado
except NoSuchElementException:
    datos_detallados['email'] = 'N/A'  # ← Agregado
```

---

## 🎯 Comportamiento Ahora

### Antes:
```csv
nombre,telefono,sitio_web,email
Empresa A,011-1234567,,
Empresa B,,,
Empresa C,011-9999999,,
```

**Problema:** Celdas vacías → no sabes si no buscaste o si realmente no tiene.

---

### Después:
```csv
nombre,telefono,sitio_web,email
Empresa A,011-1234567,N/A,N/A
Empresa B,N/A,N/A,N/A
Empresa C,011-9999999,http://web.com,N/A
```

**Ventaja:** `N/A` = **verificado pero sin datos**

---

## ✅ Beneficios

1. **Diferenciación Clara:**
   - Vacío = no procesado aún
   - `N/A` = verificado, pero no tiene ese dato

2. **Evita Re-búsquedas:**
   - El script `completar_telefonos.py` **no procesará** empresas con `N/A`
   - Solo procesará las que tengan celda vacía

3. **Estadísticas Precisas:**
   ```python
   # Con datos reales
   con_telefono = df[(df['telefono'].notna()) & (df['telefono'] != 'N/A')]
   
   # Verificados sin datos
   sin_telefono = df[df['telefono'] == 'N/A']
   
   # No procesados aún
   pendientes = df[df['telefono'].isna() | (df['telefono'] == '')]
   ```

4. **Base de Datos Más Limpia:**
   - Sabes exactamente qué empresas no tienen teléfono público
   - Puedes filtrar fácilmente

---

## 🔄 Compatibilidad con `completar_telefonos.py`

El script ya tenía esta lógica implementada:

```python
# Solo procesa empresas SIN N/A
sin_telefono = df[
    ((df['telefono'].isna()) | (df['telefono'] == '')) & 
    (df['telefono'] != 'N/A')  # ← Excluye N/A
]

# Después de buscar, si no encuentra:
if not datos_detallados.get('telefono'):
    df.at[idx, 'telefono'] = 'N/A'  # ← Marca como verificado
```

---

## 📊 Ejemplo de Resultado

```bash
Total de lugares: 1,500

Con datos encontrados:
  📞 Con teléfono: 1,200 (80%)
  🌐 Con sitio web: 900 (60%)
  📧 Con email: 150 (10%)

Verificados sin datos (N/A):
  📞 Sin teléfono: 300 (20%)
  🌐 Sin sitio web: 600 (40%)
  📧 Sin email: 1,350 (90%)
```

**Interpretación:**
- 1,200 empresas **tienen** teléfono
- 300 empresas **no tienen** teléfono (verificado)
- 0 empresas **sin verificar** (todos tienen dato o N/A)

---

## ✅ Listo

El sistema ahora **siempre** pondrá `N/A` cuando no encuentre:
- Teléfono
- Sitio web
- Email

**Ninguna celda quedará vacía después del scraping.**
