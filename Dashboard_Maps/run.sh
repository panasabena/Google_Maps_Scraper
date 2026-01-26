#!/bin/bash

# Script para ejecutar el dashboard de forma rápida
# Asegura que el entorno virtual esté activado

echo "🚀 Iniciando Dashboard de Scraping Argentina..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "app.py" ]; then
    echo "❌ Error: Debes ejecutar este script desde el directorio Dashboard_Maps"
    exit 1
fi

# Verificar que el entorno virtual existe
if [ ! -d "Dossier" ]; then
    echo "⚠️  Entorno virtual 'Dossier' no encontrado"
    echo "📦 Ejecuta primero: ./install.sh"
    exit 1
fi

# Activar entorno virtual
echo "🔌 Activando entorno virtual..."
source Dossier/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Error al activar el entorno virtual"
    exit 1
fi

# Verificar que Dash está instalado
python -c "import dash" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Dependencias no instaladas"
    echo "📥 Instalando dependencias..."
    pip install -r requirements.txt
fi

# Ejecutar la aplicación
echo "✅ Iniciando dashboard..."
echo "🌐 Accede en: http://localhost:8050/"
echo ""
echo "💡 Presiona Ctrl+C para detener el servidor"
echo ""
echo "="*60

python app.py
