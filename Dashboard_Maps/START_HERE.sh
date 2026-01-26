#!/bin/bash
# Script para iniciar el Dashboard fácilmente

cd /Users/panasabena/Scraper_Maps/Dashboard_Maps

# Activar entorno virtual
source Dossier/bin/activate

# Instalar waitress si no está
pip install waitress 2>/dev/null || true

# Iniciar dashboard
python start_dashboard.py
