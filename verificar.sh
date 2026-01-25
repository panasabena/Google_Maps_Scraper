#!/bin/bash

# Script de verificación del proyecto
# Verifica que todos los archivos estén en su lugar y sean válidos

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "🔍 VERIFICACIÓN DEL PROYECTO - Google Maps Scraper"
echo "═══════════════════════════════════════════════════════════════"
echo ""

# Colores
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
total_checks=0
passed_checks=0
failed_checks=0

check_file() {
    total_checks=$((total_checks + 1))
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        passed_checks=$((passed_checks + 1))
    else
        echo -e "${RED}✗${NC} $1 - FALTA"
        failed_checks=$((failed_checks + 1))
    fi
}

check_executable() {
    total_checks=$((total_checks + 1))
    if [ -x "$1" ]; then
        echo -e "${GREEN}✓${NC} $1 (ejecutable)"
        passed_checks=$((passed_checks + 1))
    else
        echo -e "${YELLOW}⚠${NC} $1 (no ejecutable)"
    fi
}

echo "📄 Verificando archivos de documentación..."
echo "───────────────────────────────────────────────────────────────"
check_file "README.md"
check_file "QUICKSTART.md"
check_file "ARQUITECTURA.md"
check_file "TROUBLESHOOTING.md"
check_file "INDEX.md"
echo ""

echo "🐍 Verificando scripts Python..."
echo "───────────────────────────────────────────────────────────────"
check_file "main.py"
check_file "config.py"
check_file "config_example.py"
check_file "geolocator.py"
check_file "segment_searcher.py"
check_file "detail_extractor.py"
check_file "data_manager.py"
check_file "utils.py"
check_file "test.py"
check_file "utils_cli.py"
check_file "analizar_resultados.py"
echo ""

echo "🔧 Verificando archivos de configuración..."
echo "───────────────────────────────────────────────────────────────"
check_file "requirements.txt"
check_file ".gitignore"
check_file "setup.sh"
echo ""

echo "📦 Verificando permisos de ejecución..."
echo "───────────────────────────────────────────────────────────────"
check_executable "main.py"
check_executable "test.py"
check_executable "setup.sh"
check_executable "utils_cli.py"
check_executable "analizar_resultados.py"
echo ""

echo "📂 Verificando estructura del proyecto..."
echo "───────────────────────────────────────────────────────────────"

# Contar archivos Python
python_files=$(find . -maxdepth 1 -name "*.py" | wc -l)
echo -e "${GREEN}✓${NC} Archivos Python encontrados: $python_files"

# Contar archivos de documentación
md_files=$(find . -maxdepth 1 -name "*.md" | wc -l)
echo -e "${GREEN}✓${NC} Archivos de documentación: $md_files"

echo ""

echo "🐍 Verificando sintaxis Python..."
echo "───────────────────────────────────────────────────────────────"

syntax_errors=0
for file in *.py; do
    if [ -f "$file" ]; then
        if python3 -m py_compile "$file" 2>/dev/null; then
            echo -e "${GREEN}✓${NC} $file - Sintaxis válida"
        else
            echo -e "${RED}✗${NC} $file - Error de sintaxis"
            syntax_errors=$((syntax_errors + 1))
        fi
    fi
done

if [ $syntax_errors -eq 0 ]; then
    echo -e "${GREEN}✓${NC} Todos los archivos Python tienen sintaxis válida"
else
    echo -e "${RED}✗${NC} $syntax_errors archivo(s) con errores de sintaxis"
fi

echo ""

echo "📊 Verificando imports..."
echo "───────────────────────────────────────────────────────────────"

# Verificar que los módulos propios se importen correctamente
if python3 -c "from config import CONFIG; from utils import setup_logging; from geolocator import Geolocator" 2>/dev/null; then
    echo -e "${GREEN}✓${NC} Los módulos propios se importan correctamente"
    passed_checks=$((passed_checks + 1))
else
    echo -e "${YELLOW}⚠${NC} Algunos módulos tienen problemas de importación (normal si no están instaladas las dependencias)"
fi

total_checks=$((total_checks + 1))

echo ""
echo "═══════════════════════════════════════════════════════════════"
echo "📊 RESUMEN"
echo "═══════════════════════════════════════════════════════════════"
echo -e "Total de verificaciones: $total_checks"
echo -e "${GREEN}Exitosas: $passed_checks${NC}"
echo -e "${RED}Fallidas: $failed_checks${NC}"
echo ""

percentage=$((passed_checks * 100 / total_checks))

if [ $failed_checks -eq 0 ]; then
    echo -e "${GREEN}✅ PROYECTO VERIFICADO - 100% OK${NC}"
    echo ""
    echo "El proyecto está listo para usar."
    echo "Siguiente paso:"
    echo "  1. Ejecuta: bash setup.sh"
    echo "  2. O instala manualmente: python3 -m venv scraper && source scraper/bin/activate && pip install -r requirements.txt"
    echo ""
elif [ $percentage -ge 80 ]; then
    echo -e "${YELLOW}⚠️  PROYECTO CASI COMPLETO - ${percentage}% OK${NC}"
    echo ""
    echo "Hay algunos archivos faltantes o problemas menores."
    echo "El proyecto debería funcionar, pero verifica los archivos faltantes."
    echo ""
else
    echo -e "${RED}❌ PROYECTO INCOMPLETO - ${percentage}% OK${NC}"
    echo ""
    echo "Faltan archivos importantes. Verifica la instalación."
    echo ""
fi

echo "Para más información:"
echo "  - README.md: Documentación completa"
echo "  - QUICKSTART.md: Guía rápida"
echo "  - INDEX.md: Índice de toda la documentación"
echo ""
echo "═══════════════════════════════════════════════════════════════"
echo ""
