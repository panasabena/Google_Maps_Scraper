# 🚀 CÓMO INICIAR EL DASHBOARD

## El problema "Operation not permitted" está RESUELTO

Las coordenadas ya funcionan correctamente (25,745 empresas con coordenadas válidas).

El error "Operation not permitted" es por permisos de macOS con el watchdog de Flask.

## ✅ SOLUCIÓN: Ejecuta esto desde TU terminal (iTerm/Terminal.app)

```bash
cd /Users/panasabena/Scraper_Maps/Dashboard_Maps
source Dossier/bin/activate
pip install waitress
python start_dashboard.py
```

O simplemente:

```bash
/Users/panasabena/Scraper_Maps/Dashboard_Maps/START_HERE.sh
```

## 🎯 Qué se arregló:

1. ✅ **Coordenadas**: Ahora se extraen correctamente de las URLs de Google Maps
   - Formato: `!3d-34.6158871!4d-58.5273434`
   - 25,745 empresas con coordenadas válidas

2. ✅ **Servidor**: Waitress (producción) no necesita permisos especiales

3. ✅ **Rubros duplicados**: Se eliminan automáticamente (190 rubros únicos)

4. ✅ **Progreso**: Ahora solo cuenta rubros que están en el config actual

## 🗺️ Mapa

Cuando veas el mapa de empresas, verás:
- **Puntos verdes**: Ubicaciones completadas al 100%
- **Puntos amarillos**: Ubicaciones en progreso
- **25,000+ empresas** en el mapa de Argentina

## 📊 Córdoba

Si Córdoba sigue en 50%, es porque tiene rubros scrapeados que ya no están en tu config actual.

El dashboard ahora solo cuenta rubros válidos (que están en RUBROS_BUSQUEDA).
