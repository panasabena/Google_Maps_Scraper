#!/bin/bash

# Script de instalación y configuración del entorno virtual

echo "🚀 Instalación del Scraper de Google Maps"
echo "=========================================="
echo ""

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"
echo ""

# Crear entorno virtual
echo "📦 Creando entorno virtual 'scraper'..."
python3 -m venv scraper

if [ $? -ne 0 ]; then
    echo "❌ Error creando el entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual creado"
echo ""

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source scraper/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error activando el entorno virtual"
    exit 1
fi

echo "✅ Entorno virtual activado"
echo ""

# Actualizar pip
echo "⬆️  Actualizando pip..."
pip install --upgrade pip

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error instalando dependencias"
    exit 1
fi

echo ""
echo "✅ Dependencias instaladas correctamente"
echo ""

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p resultados backups logs
echo "✅ Directorios creados"
echo ""

# Ejecutar tests
echo "🧪 Ejecutando tests..."
python test.py

if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  Algunos tests fallaron, pero el entorno está configurado"
fi

echo ""
echo "=========================================="
echo "✅ Instalación completada"
echo "=========================================="
echo ""
echo "Para usar el scraper:"
echo "  1. Activa el entorno virtual: source scraper/bin/activate"
echo "  2. Edita config.py para personalizar la búsqueda"
echo "  3. Ejecuta: python main.py"
echo ""
echo "Para más información, consulta README.md"
echo ""
