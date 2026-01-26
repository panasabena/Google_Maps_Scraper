#!/usr/bin/env python3
"""
Inicia el Dashboard usando Waitress (servidor de producción)
Resuelve el problema de "Operation not permitted" en macOS
"""

print("\n" + "="*60)
print("🚀 Iniciando Dashboard de Monitoreo de Scraping Argentina")
print("="*60)

try:
    from waitress import serve
    from app import app
    
    print("✅ Usando servidor Waitress (producción)")
    print("🌐 Dashboard disponible en: http://127.0.0.1:8050")
    print("⏹️  Presiona Ctrl+C para detener")
    print("="*60 + "\n")
    
    serve(app.server, host='127.0.0.1', port=8050, threads=4)
    
except ImportError:
    print("⚠️  Waitress no está instalado. Instalando...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "waitress"])
    print("✅ Waitress instalado. Ejecuta este script nuevamente.")
    
except KeyboardInterrupt:
    print("\n\n👋 Dashboard detenido correctamente")
    
except Exception as e:
    print(f"\n❌ Error al iniciar el dashboard: {e}")
    print("\n📋 Intenta ejecutar manualmente:")
    print("   cd /Users/panasabena/Scraper_Maps/Dashboard_Maps")
    print("   source Dossier/bin/activate")
    print("   pip install waitress")
    print("   python start_dashboard.py")
