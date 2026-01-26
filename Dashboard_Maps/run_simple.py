#!/usr/bin/env python3
"""Script simple para iniciar el dashboard sin watchdog"""

import os
# NO setear WERKZEUG_RUN_MAIN

from app import app, DASHBOARD_CONFIG

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Dashboard de Monitoreo de Scraping Argentina")
    print("="*60)
    print(f"🌐 Abriendo en http://127.0.0.1:{DASHBOARD_CONFIG['port']}/")
    print("="*60 + "\n")
    
    app.run(
        debug=False,
        use_reloader=False,
        dev_tools_hot_reload=False,
        port=DASHBOARD_CONFIG['port'],
        host='127.0.0.1'
    )
