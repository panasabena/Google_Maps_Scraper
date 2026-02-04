# 🚀 GUÍA RÁPIDA - Email Marketing Sin Tracking

## 📦 Sistema Simple de Envío de Emails

Este sistema envía emails profesionales y personalizados **sin tracking**, lo cual mejora la deliverability y hace que lleguen a la bandeja "Principal" en lugar de "Promociones".

---

## ⚡ INICIO RÁPIDO

### Paso 1: Editar tu lista de contactos

Abre `contactos_empresas.csv` y agrega tus contactos:

```csv
email,nombre_empresa
contacto@empresa1.com,Empresa 1 SRL
info@empresa2.com,Consultora ABC
ventas@empresa3.com,Servicios XYZ
```

### Paso 2: Ejecutar el script

```bash
cd /Users/panasabena/Scraper_Maps/Emailing
python email_sender.py
```

### Paso 3: Seleccionar modo test

```
1. MODO TEST (primeros 2 contactos)
```

Escribe `1` y luego `si` para confirmar.

### Paso 4: Revisar tu email

Abre tu bandeja de entrada y verifica que el email se vea bien y esté en "Principal".

### Paso 5: Enviar a todos (opcional)

Si todo está bien, vuelve a ejecutar y selecciona opción `2`.

---

## 📝 Formato del CSV

Tu CSV debe tener **exactamente estas columnas**:

```csv
email,nombre_empresa
contacto@empresa1.com,Empresa 1 SRL
info@empresa2.com,Consultora ABC
ventas@empresa3.com,Servicios XYZ Ltda
```

**Notas:**
- Usa **comas** como separador (no punto y coma)
- Primera fila son los nombres de columna
- No dejes espacios extra antes o después de los valores

---

## ✨ Características del Sistema

### ✅ Sin Tracking
- No hay pixel de seguimiento
- No hay links de tracking
- Parece un email personal
- Mayor probabilidad de llegar a "Principal"

### ⏱️ Delays Automáticos
- Espera 30-60 segundos entre cada email (aleatorio)
- Parece que los envías manualmente
- Gmail no detecta envío masivo

### 🎨 Template Profesional
- Diseño limpio y personal
- No parece marketing
- HTML responsive
- Links simples (no botones gigantes)

### 📊 Límites Recomendados
- **50-100 emails por día** (máximo recomendado)
- **No más de 50 por hora**
- **Gmail límite:** 500 emails/día (cuenta gratuita)

---

## 🎯 Mejores Prácticas

### 1. Horarios de Envío
- ✅ Martes a Jueves
- ✅ 10:00 AM - 2:00 PM
- ❌ Evita lunes temprano y viernes tarde
- ❌ No envíes fines de semana

### 2. Volumen Diario
```
Día 1: 10-20 emails (calentar la cuenta)
Día 2: 30-40 emails
Día 3+: 50-100 emails (máximo)
```

**¿Por qué "calentar"?** Si empiezas enviando 100 emails el primer día, Gmail puede marcarte como spam.

### 3. Personalización
El script ya personaliza automáticamente:
- ✅ Nombre de la empresa en el mensaje
- ✅ Email individual para cada contacto
- ✅ Subject line personalizable

### 4. Seguimiento
Como no hay tracking automático:
- Revisa tu bandeja de entrada manualmente
- Responde rápido a las respuestas
- Anota quién respondió en una hoja de cálculo
- Haz follow-up manual en 3-4 días

---

## 🔐 Seguridad

⚠️ **Tu contraseña de Gmail está en el código**

Para mayor seguridad, puedes cambiar esto en `email_sender.py`:

```python
# Línea actual (menos seguro):
EMAIL_PASSWORD = 'tvnh yezh ifiy egwt'

# Cambiar a (más seguro):
import getpass
EMAIL_PASSWORD = getpass.getpass("Contraseña de Gmail: ")
```

---

## 🐛 Problemas Comunes

### "Authentication failed"
→ Verifica tu contraseña de aplicación de Gmail
→ Asegúrate de tener activada la verificación en 2 pasos

### "No se encontró el archivo CSV"
→ Verifica la ruta del archivo
→ Asegúrate de estar en la carpeta correcta

### "El CSV debe tener las columnas..."
→ Verifica que tu CSV tenga `email` y `nombre_empresa`
→ Usa comas, no punto y coma

### Los emails van a spam
→ Envía menos emails por día
→ Calienta tu cuenta gradualmente
→ Evita palabras spam en el subject ("GRATIS", "OFERTA", etc.)

### Emails llegan a "Promociones"
→ El script está optimizado para ir a "Principal"
→ Si aún así van a Promociones, es porque Gmail detectó patrones
→ Reduce el volumen diario y espacia más los envíos

---

## 📊 Métricas (Manual)

Sin tracking automático, lleva un registro manual en una hoja de cálculo:

```
| Email              | Empresa       | Enviado    | Respondió | Interesado |
|--------------------|---------------|------------|-----------|------------|
| info@empresa1.com  | Empresa 1     | 2026-02-01 | ✓         | Sí         |
| ventas@empresa2.com| Empresa 2     | 2026-02-01 | ✗         | -          |
| contacto@empresa3  | Empresa 3     | 2026-02-01 | ✓         | No         |
```

---

## 🎨 Personalizar el Template

Para cambiar el mensaje del email, edita `email_sender.py`:

1. Busca la función `obtener_template_html()`
2. Modifica el texto según necesites
3. También actualiza `obtener_texto_plano()` con el mismo contenido

**Mantén:**
- ✅ Diseño simple y limpio
- ✅ Sin mucho color
- ✅ Links de texto (no botones gigantes)
- ✅ Firma personal al final

---

## 💡 Tips Finales

1. **Prueba primero**: Siempre envía a tu propio email primero
2. **Menos es más**: 50 emails bien dirigidos > 500 genéricos
3. **Personaliza**: Menciona algo específico de su empresa si puedes
4. **Sé paciente**: No todos responden, 5-10% de respuesta es bueno
5. **Haz seguimiento**: El segundo email tiene más apertura

---

## 📞 Soporte

**Alfredo Sabena**
- 📧 panasabena@gmail.com
- 📱 3515173052
- 📅 https://calendly.com/alfre-sabena/30min
