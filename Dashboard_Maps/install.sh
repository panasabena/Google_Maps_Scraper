#!/bin/bash

# Script de instalación y configuración del Dashboard de Scraping Argentina

echo "============================================================"
echo "🚀 Instalación del Dashboard de Scraping Argentina"
echo "============================================================"
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Este script debe ejecutarse desde el directorio Dashboard_Maps"
    exit 1
fi

# Verificar Python
echo "📌 Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor, instala Python 3.8 o superior."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python encontrado: $PYTHON_VERSION"
echo ""

# Crear entorno virtual "Dossier"
echo "📦 Creando entorno virtual 'Dossier'..."
if [ -d "Dossier" ]; then
    echo "⚠️  El entorno virtual 'Dossier' ya existe"
    read -p "¿Deseas recrearlo? (s/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Ss]$ ]]; then
        echo "🗑️  Eliminando entorno virtual existente..."
        rm -rf Dossier
        python3 -m venv Dossier
        echo "✅ Entorno virtual recreado"
    else
        echo "✅ Usando entorno virtual existente"
    fi
else
    python3 -m venv Dossier
    echo "✅ Entorno virtual 'Dossier' creado"
fi
echo ""

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source Dossier/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✅ pip actualizado"
echo ""

# Instalar dependencias
echo "📥 Instalando dependencias..."
echo "   Esto puede tomar unos minutos..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error al instalar dependencias"
    exit 1
fi

echo "✅ Dependencias instaladas correctamente"
echo ""

# Crear directorios necesarios
echo "📁 Creando directorios necesarios..."
mkdir -p data/geo
mkdir -p assets/css
mkdir -p assets/images
mkdir -p logs

echo "✅ Directorios creados"
echo ""

# Verificar archivos de datos
echo "🔍 Verificando archivos de datos..."

CSV_PATH="/Users/panasabena/Scraper_Maps/resultados/google_maps_results.csv"
JSON_PATH="/Users/panasabena/Scraper_Maps/estado_ejecucion.json"

if [ -f "$CSV_PATH" ]; then
    echo "✅ CSV encontrado: $CSV_PATH"
    NUM_LINES=$(wc -l < "$CSV_PATH")
    echo "   📊 Líneas en CSV: $NUM_LINES"
else
    echo "⚠️  CSV no encontrado: $CSV_PATH"
    echo "   El dashboard puede no mostrar datos"
fi

if [ -f "$JSON_PATH" ]; then
    echo "✅ JSON encontrado: $JSON_PATH"
else
    echo "⚠️  JSON no encontrado: $JSON_PATH"
    echo "   El progreso puede no mostrarse correctamente"
fi
echo ""

# Verificar GeoJSON
if [ -f "data/geo/argentina_provincias.geojson" ]; then
    echo "✅ GeoJSON de provincias encontrado"
else
    echo "⚠️  GeoJSON de provincias no encontrado"
fi
echo ""

# Resumen de instalación
echo "============================================================"
echo "✅ Instalación completada"
echo "============================================================"
echo ""
echo "📝 Para iniciar el dashboard:"
echo ""
echo "   1. Asegúrate de que el entorno virtual esté activado:"
echo "      source Dossier/bin/activate"
echo ""
echo "   2. Ejecuta la aplicación:"
echo "      python app.py"
echo ""
echo "   3. Abre tu navegador en:"
echo "      http://localhost:8050/"
echo ""
echo "============================================================"
echo ""

# Preguntar si desea iniciar ahora
read -p "¿Deseas iniciar el dashboard ahora? (s/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "🚀 Iniciando dashboard..."
    echo ""
    python app.py
fi
