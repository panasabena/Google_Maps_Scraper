# 📧 Sistema de Email Marketing Simple

Sistema de envío de emails profesionales **sin tracking**, optimizado para llegar a la bandeja "Principal" en lugar de "Promociones".

---

## 🎯 Características

- ✅ **Sin tracking** - Mayor deliverability
- ✅ **Delays automáticos** - Parece envío manual
- ✅ **Template profesional** - Diseño limpio y personal
- ✅ **Personalización** - Nombre de empresa automático
- ✅ **Gmail directo** - Envía desde tu cuenta personal

---

## 🚀 Uso Rápido

```bash
# 1. Edita contactos_empresas.csv con tus contactos
email,nombre_empresa
contacto@empresa1.com,Empresa 1 SRL

# 2. Ejecuta el script
python email_sender.py

# 3. Selecciona MODO TEST primero
Opción: 1

# 4. Revisa el email en tu bandeja de entrada

# 5. Si todo está bien, envía a todos
python email_sender.py
Opción: 2
```

---

## 📁 Archivos del Sistema

```
Emailing/
├── email_sender.py           # Script principal ⭐
├── email_template.html       # Template de referencia
├── contactos_empresas.csv    # Tu lista de contactos
├── GUIA_RAPIDA.md           # Guía paso a paso
└── requirements.txt          # (vacío - no necesita dependencias)
```

---

## 📝 Formato del CSV

```csv
email,nombre_empresa
contacto@empresa1.com,Empresa 1 SRL
info@empresa2.com,Consultora ABC
ventas@empresa3.com,Servicios XYZ
```

**Columnas requeridas:**
- `email` - Email del contacto
- `nombre_empresa` - Nombre de la empresa (se personaliza automáticamente)

---

## ⚙️ Configuración Inicial

### 1. Contraseña de Aplicación de Gmail

El script usa una **contraseña de aplicación** de Gmail (no tu contraseña normal).

**Ya está configurada** con `panasabena@gmail.com`, pero si necesitas cambiarla:

1. Ve a [Seguridad de Google](https://myaccount.google.com/security)
2. Activa "Verificación en 2 pasos"
3. Ve a "Contraseñas de aplicaciones"
4. Genera una nueva contraseña
5. Reemplázala en `email_sender.py` línea ~16:
   ```python
   EMAIL_PASSWORD = 'tu nueva contraseña aqui'
   ```

### 2. Límites de Gmail

- **Cuenta gratuita:** 500 emails/día
- **Google Workspace:** 2000 emails/día
- **Recomendado:** 50-100 emails/día para mejor deliverability

---

## 🎯 Mejores Prácticas

### Volumen de Envío

```
Día 1: 10-20 emails    (calentar cuenta)
Día 2: 30-40 emails
Día 3+: 50-100 emails  (máximo recomendado)
```

### Horarios Óptimos

- ✅ **Martes a Jueves**
- ✅ **10:00 AM - 2:00 PM**
- ❌ Evita lunes temprano
- ❌ Evita viernes tarde
- ❌ No envíes fines de semana

### Delays entre Envíos

El script espera **30-60 segundos** entre cada email automáticamente para:
- Parecer envío manual
- No activar filtros de spam de Gmail
- Mejor deliverability

---

## 📊 Sin Tracking = Mejor Deliverability

### ¿Por qué NO usar tracking?

**Emails CON tracking:**
- Van a "Promociones" o "Suscripciones"
- Gmail detecta headers de marketing
- Menor tasa de apertura
- Parece campaña masiva

**Emails SIN tracking (este sistema):**
- Van a "Principal" (inbox)
- Parece email personal
- Mayor tasa de apertura
- Mejor para B2B

### ¿Cómo hacer seguimiento entonces?

**Manual, pero efectivo:**
1. Revisa respuestas en tu Gmail
2. Anota quiénes respondieron en una hoja de cálculo
3. Haz follow-up manual en 3-4 días
4. Para <100 emails/día, es totalmente manejable

---

## 🎨 Personalizar el Mensaje

Para cambiar el contenido del email:

1. Abre `email_sender.py`
2. Busca las funciones:
   - `obtener_template_html()` - Versión HTML
   - `obtener_texto_plano()` - Versión texto
3. Modifica el contenido
4. Mantén el diseño simple (sin botones gigantes, poco color)

---

## ⚠️ Consejos Importantes

### 1. Siempre Prueba Primero
```bash
# Envía a tu propio email antes de enviar a clientes
python email_sender.py
Opción: 1  # MODO TEST
```

### 2. Calienta tu Cuenta
Si nunca has enviado emails masivos desde tu Gmail:
- Día 1: Solo 10-20 emails
- Aumenta gradualmente cada día
- Gmail puede marcar como spam si empiezas con 100 emails

### 3. Evita Palabras Spam
En el asunto y contenido, evita:
- ❌ GRATIS, OFERTA, PROMOCIÓN
- ❌ URGENTE, AHORA, HOY
- ❌ Muchos signos de exclamación!!!
- ❌ Todo en MAYÚSCULAS

### 4. Responde Rápido
- Revisa tu bandeja varias veces al día
- Responde rápido a los interesados
- Esto mejora tu reputación de envío

---

## 🐛 Solución de Problemas

### Error: "Authentication failed"
→ Verifica contraseña de aplicación de Gmail
→ Asegúrate de tener 2FA activada

### Emails van a spam
→ Reduce volumen diario (20-30 emails)
→ Calienta tu cuenta gradualmente
→ Revisa que no uses palabras spam

### Emails van a "Promociones"
→ Es raro con este sistema, pero puede pasar
→ Reduce aún más el volumen
→ Espacía más los envíos (aumenta delays)

### "No such file"
→ Verifica que `contactos_empresas.csv` exista
→ Verifica que estés en la carpeta correcta

---

## 📈 Expectativas Realistas

### Tasas Típicas para B2B:

- **Tasa de apertura:** 20-30%
- **Tasa de respuesta:** 5-10%
- **Conversión a reunión:** 1-3%

**Ejemplo con 100 emails:**
- 20-30 personas abrirán el email
- 5-10 responderán
- 1-3 agendar��n reunión

Esto es **NORMAL y BUENO** para cold outreach B2B.

---

## 🎯 Estrategia Recomendada

### Secuencia de Emails

**Email 1 (este script):**
- Introducción y propuesta de valor
- Link a Calendly
- Espera 3-4 días

**Email 2 (follow-up manual):**
- Referencia al email anterior
- Agrega algo de valor (caso de éxito, dato relevante)
- Pregunta simple

**Email 3 (último intento):**
- Último contacto
- Ofrece algo específico
- Opción de darse de baja

---

## 📞 Soporte

**Alfredo Sabena**
- 📧 panasabena@gmail.com
- 📱 3515173052
- 📅 https://calendly.com/alfre-sabena/30min

---

## 📄 Archivos de Referencia

- `GUIA_RAPIDA.md` - Tutorial paso a paso
- `ENTORNO_VIRTUAL.md` - Info del entorno virtual (opcional, no necesario)
- `email_template.html` - Template de referencia para ver el HTML completo

---

## ✨ ¿Por qué este sistema es mejor que Brevo?

| Característica | Este Sistema | Brevo |
|----------------|-------------|-------|
| Va a "Principal" | ✅ Sí | ❌ No (va a Promociones) |
| Parece personal | ✅ Sí | ❌ No |
| Tracking | ❌ No | ✅ Sí |
| Costo | 💚 Gratis | 💰 Gratis hasta 300/día |
| Setup | 🟢 Muy fácil | 🟡 Medio |
| Límite | 500/día | 300/día (gratis) |
| Mejor para | B2B Outreach | Newsletter masiva |

**Conclusión:** Para contactar empresas B2B (tu caso), este sistema es superior porque llega a "Principal" y parece más personal.

---

¡Listo para enviar emails profesionales! 🚀
