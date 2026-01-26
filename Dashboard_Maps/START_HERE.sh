#!/bin/bash
# Script para iniciar el Dashboard fácilmente

# Obtener el directorio donde está este script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Activar entorno virtual
source Dossier/bin/activate

# Instalar waitress si no está
pip install waitress 2>/dev/null || true

# Iniciar dashboard
python start_dashboard.py
