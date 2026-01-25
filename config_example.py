"""
Ejemplo de configuración personalizada
Copia este archivo y personalízalo según tus necesidades
"""

# CONFIGURACIÓN DE BÚSQUEDA
CONFIG = {
    # ========================================
    # UBICACIÓN Y RUBROS
    # ========================================
    
    # Ubicación a buscar (debe ser reconocible por OpenStreetMap)
    'ubicacion': "Córdoba, Argentina",
    # Otras opciones:
    # 'ubicacion': "Buenos Aires, Argentina",
    # 'ubicacion': "Rosario, Santa Fe, Argentina",
    # 'ubicacion': "Madrid, España",
    
    # Rubros/categorías a buscar
    'rubros': [
        "fabrica",
        "logistica", 
        "transportes",
        "mudanzas",
        "fletes",
        "agencia de marketing",
        "higiene y seguridad",
        "auditores",
        "cadetería"
    ],
    # Puedes agregar más rubros según tu necesidad:
    # "restaurante", "hotel", "gimnasio", "ferretería", etc.
    
    # ========================================
    # SEGMENTACIÓN GEOGRÁFICA
    # ========================================
    
    # Tamaño de la cuadrícula para dividir el área
    # 2 = 2x2 = 4 segmentos
    # 3 = 3x3 = 9 segmentos
    # 4 = 4x4 = 16 segmentos
    # A mayor grid_size, más cobertura pero más tiempo
    'grid_size': 2,
    
    # Nivel de zoom en Google Maps (10-16 recomendado)
    # 10 = muy alejado (ciudad completa)
    # 13 = zoom medio (barrios)
    # 16 = muy cerca (calles específicas)
    'zoom_level': 13,
    
    # ========================================
    # LÍMITES Y CONTROL
    # ========================================
    
    # Máximo de resultados por rubro (por segmento)
    'max_resultados_por_rubro': 1000,
    
    # Máximo de scrolls por página de resultados
    # Cada scroll carga ~20 resultados
    # 20 scrolls = ~400 resultados máximo
    'max_scrolls_por_pagina': 20,
    
    # Máximo de empresas a extraer por día (límite de seguridad)
    'max_empresas_dia': 2000,
    
    # ========================================
    # DELAYS (en segundos)
    # ========================================
    # Importantes para evitar detección
    
    'delays': {
        # Tiempo entre segmentos (rango mínimo-máximo)
        'entre_segmentos': (8, 15),
        
        # Tiempo entre rubros
        'entre_rubros': (4, 8),
        
        # Tiempo después de cada scroll
        'despues_scroll': (2, 4),
        
        # Tiempo de carga inicial de página
        'carga_inicial': (3, 6)
    },
    
    # ========================================
    # ANTI-DETECCIÓN
    # ========================================
    
    # Rotar User-Agent cada N solicitudes
    'user_agent_rotation': 50,
    
    # Ejecutar sin interfaz gráfica (headless)
    # False = ver el navegador (recomendado para debugging)
    # True = ejecutar en segundo plano
    'headless': False,
    
    # ========================================
    # EXPORTACIÓN Y CHECKPOINTS
    # ========================================
    
    # Guardar checkpoint cada X empresas extraídas
    'checkpoint_cada': 20,
    
    # Formato de salida ('excel' o 'csv')
    'formato_salida': 'excel',
    
    # Nombre del archivo de salida
    'archivo_excel': 'google_maps_results.xlsx',
    
    # ========================================
    # DIRECTORIOS
    # ========================================
    
    'dir_resultados': 'resultados',
    'dir_backups': 'backups',
    'dir_logs': 'logs',
    
    # ========================================
    # ARCHIVOS DE ESTADO
    # ========================================
    
    'archivo_estado': 'estado_ejecucion.json',
    'archivo_cookies': 'cookies.pkl'
}

# ============================================================
# CONFIGURACIÓN PARA CASOS ESPECÍFICOS
# ============================================================

# EJEMPLO 1: Búsqueda rápida (pocos rubros, área pequeña)
CONFIG_RAPIDA = {
    **CONFIG,
    'rubros': ["restaurante", "cafetería"],
    'grid_size': 1,  # Sin división
    'max_scrolls_por_pagina': 10,
    'delays': {
        'entre_segmentos': (5, 8),
        'entre_rubros': (3, 5),
        'despues_scroll': (1, 2),
        'carga_inicial': (2, 4)
    }
}

# EJEMPLO 2: Búsqueda exhaustiva (muchos rubros, área grande)
CONFIG_EXHAUSTIVA = {
    **CONFIG,
    'grid_size': 4,  # 16 segmentos
    'max_scrolls_por_pagina': 30,
    'delays': {
        'entre_segmentos': (15, 25),
        'entre_rubros': (8, 12),
        'despues_scroll': (3, 5),
        'carga_inicial': (4, 7)
    }
}

# EJEMPLO 3: Búsqueda nocturna (delays más largos, headless)
CONFIG_NOCTURNA = {
    **CONFIG,
    'headless': True,
    'delays': {
        'entre_segmentos': (20, 35),
        'entre_rubros': (10, 15),
        'despues_scroll': (3, 6),
        'carga_inicial': (5, 8)
    }
}

# ============================================================
# PARA USAR UNA CONFIGURACIÓN ESPECÍFICA:
# ============================================================
# En main.py, importa la configuración deseada:
# from config_example import CONFIG_RAPIDA as CONFIG
# o
# from config_example import CONFIG_EXHAUSTIVA as CONFIG
