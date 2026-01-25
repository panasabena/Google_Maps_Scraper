"""
Configuración del scraper de Google Maps
"""

CONFIG = {
    # Búsqueda
    'rubros': [
    "fabrica",
    "logistica", 
    "transportes",
    "mudanzas",
    "fletes",
    "agencia de marketing",
    "higiene y seguridad",
    "auditores",
    "cadetería",
    
    # ✅ AGREGAR AQUÍ tus nuevos rubros:
    "carpintería",
    "herrería",
    "electricista",
    "plomero",
    "pintor",
    "consultoría",
    "software",
    "diseño gráfico",
    "estudio de ingeniería",
"consultoría ingeniería",
"ingeniería civil",
"ingenieros consultores",
"proyectos de ingeniería",
"clínica médica",
"consultorio médico",
"centro de salud",
"policlínico",
"consultorio particular",
"estudio jurídico",
"despacho de abogados",
"abogados especializados",
"bufete de abogados",
"asesoría legal",
"estudio contable",
"contador público",
"auditoría contable",
"asesoría impositiva",
"contador independiente",
"agencia de marketing",
"marketing digital",
"publicidad y propaganda",
"comunicación integral",
"agencias de publicidad",
    "desarrollo de software",
    "empresa de sistemas",
"software a medida",
"desarrolladores web",
"aplicaciones móviles",
"empresa de logística",
"transporte de cargas",
"fletes y mudanzas",
"distribución logística",
"empresa de transportes",
"empresa constructora",
"construcción civil",
"obras y construcciones",
"constructoras medianas",
"empresas de construcción",
"instituto educativo",
"centro de capacitación",
"academia especializada",
"escuela de oficios",
"centro de formación",
"taller mecánico especializado",
"mecánica industrial",
"mantenimiento de maquinaria",
"reparaciones mecánicas",
"taller de maquinaria",
"mantenimiento industrial",
"servicios industriales",
"mantenimiento predictivo",
"empresas de mantenimiento",
"servicios técnicos industriales",
"agencias de viajes corporativas",
"viajes de empresa",
"turismo empresarial",
"agencias de viaje",
"estudio de arquitectura",
"arquitectos independientes",
"proyectos arquitectónicos",
"diseño arquitectónico",
"energías renovables",
"paneles solares",
"energía solar",
"instalaciones solares",
"energías sustentables",
"laboratorio de análisis",
"análisis clínicos",
"laboratorio químico",
"análisis de suelos",
"laboratorios especializados",
"empresas de seguridad",
"vigilancia y seguridad",
"seguridad privada",
"monitoreo de alarmas",
"consultoría ambiental",
"estudios ambientales",
"impacto ambiental",
"consultores ambientales",
"catering empresarial",
"servicios de catering",
"viandas empresariales",
"catering para empresas",
"administración de consorcios",
"gerencias de condominios",
"administradoras de edificios",
"consorcios y administración",
"diseño gráfico",
"diseño web",
"estudio de diseño",
"diseñadores gráficos",
"agencias de diseño",
"limpieza comercial",
"empresas de limpieza",
"servicios de limpieza",
"limpieza de oficinas",
"limpieza empresarial",
"gimnasios",
"centros de entrenamiento",
"entrenadores personales",
"fitness center",
"gymnasio",
"productora audiovisual",
"producción de videos",
"empresas de video",
"producciones audiovisuales",
"instalaciones eléctricas",
"electricistas industriales",
"empresas de electricidad",
"montajes eléctricos",
"consultoría de recursos humanos",
"recursos humanos",
"selección de personal",
"headhunting",
"reclutamiento",
"paisajismo",
"jardinería",
"mantenimiento de espacios verdes",
"diseño de jardines",
"clínica veterinaria",
"veterinarios",
"hospital veterinario",
"consultorio veterinario",
"traducción e interpretación",
"traductores públicos",
"servicios de traducción",
"agencias de traducción",
"desarrolladores inmobiliarios",
"empresas inmobiliarias",
"inversiones inmobiliarias",
"proyectos inmobiliarios",
"cooperativas",
"asociaciones cooperativas",
"cooperativa de trabajo",
"cooperativa agrícola",
"fumigación",
"control de plagas",
"desinfección",
"empresas de fumigación",
"headhunting",
"reclutamiento ejecutivo",
"agencias de reclutamiento",
"selección ejecutiva",
"fotógrafos profesionales",
"estudio de fotografía",
"fotografía empresarial",
"fotógrafos comerciales",
"análisis de suelos",
"laboratorio de suelos",
"análisis de aguas",
"estudios geotécnicos",
"compliance",
"consultoría normativa",
"regulaciones",
"cumplimiento normativo",
"montaje de exposiciones",
"stands feriales",
"montajes comerciales",
"exposiciones y ferias",
"calibración de instrumentos",
"laboratorio de calibración",
"instrumentación industrial",
"calibraciones certificadas",
"digitalización documental",
"escaneo de documentos",
"gestión documental",
"archivo digital",
"consultoría de franquicias",
"franquicias",
"desarrollo de franquicias",
"asesoría en franquicias",
"gestión deportiva",
"representantes de deportistas",
"agencias deportivas",
"management deportivo",
],
    
    # Ubicaciones (múltiples ciudades de Argentina)
    'ubicaciones': [
        "Buenos Aires, Argentina",
        "Córdoba, Argentina",
        "Rosario, Argentina",
        "Mendoza, Argentina",
        "Tucumán, Argentina",
        "La Plata, Argentina",
        "Mar del Plata, Argentina",
        "Salta, Argentina",
        "Santa Fe, Argentina",
        "Resistencia, Argentina",
        "Santiago del Estero, Argentina",
        "Corrientes, Argentina",
        "Neuquén, Argentina",
        "Bahía Blanca, Argentina",
        "San Salvador de Jujuy, Argentina",
        "Posadas, Argentina",
        "Paraná, Argentina",
        "San Luis, Argentina",
        "Río Gallegos, Argentina",
        "Comodoro Rivadavia, Argentina",
        "Ushuaia, Argentina",
        "Formosa, Argentina",
        "Quilmes, Argentina",
        "Morón, Argentina",
        "San Martín, Argentina",
        "Lanús, Argentina",
        "Lomas de Zamora, Argentina",
        "Tigre, Argentina",
        "Pilar, Argentina",
    ],
    
    # Ubicación (deprecado - ahora usa 'ubicaciones')
    'ubicacion': "Córdoba, Argentina",  # Para retrocompatibilidad
    
    # Segmentación
    # IMPORTANTE: grid_size = 1 significa NO dividir el área (1x1 = 1 segmento)
    # Si pones grid_size = 2, dividirá la ciudad en 4 cuadrantes (2x2)
    # Esto puede causar que extraiga lugares repetidos de diferentes zonas
    # RECOMENDACIÓN: Deja grid_size = 1 a menos que necesites cobertura muy específica por zonas
    'grid_size': 1,  # 1x1 = 1 segmento (sin división, cubre toda el área de una vez)
    'zoom_level': 11,  # Nivel de zoom en Google Maps (10-12 para ciudad completa, 13-16 para barrios específicos)
    
    # Límites
    'max_resultados_por_rubro': 1000,
    'max_scrolls_por_pagina': 50,  # Aumentado de 20 a 50 para más resultados
    'max_empresas_dia': 2000,
    
    # Delays (segundos)
    'delays': {
        'entre_segmentos': (8, 15),
        'entre_rubros': (4, 8),
        'despues_scroll': (3, 5),  # Aumentado de (2,4) a (3,5) para mejor scroll
        'carga_inicial': (4, 7)     # Aumentado de (3,6) a (4,7)
    },
    
    # Anti-detección
    'user_agent_rotation': 50,  # Rotar cada 50 solicitudes
    'headless': False,  # Mejor no usar headless para Google
    
    # Exportación
    'checkpoint_cada': 20,  # empresas
    'formato_salida': 'excel',  # 'excel' o 'csv'
    'archivo_excel': 'google_maps_results.xlsx',
    
    # Directorios
    'dir_resultados': 'resultados',
    'dir_backups': 'backups',
    'dir_logs': 'logs',
    
    # Estado
    'archivo_estado': 'estado_ejecucion.json',
    'archivo_cookies': 'cookies.pkl'
}

# Selectores CSS/XPath para Google Maps
SELECTORS = {
    # Contenedor de resultados
    'resultados_feed': "div[role='feed']",
    'resultados_feed_xpath': "//div[@role='feed']",
    
    # Elementos individuales de lugares
    'lugar_elemento': "//div[@role='feed']//div[contains(@class, 'Nv2PK')]",
    'lugar_elemento_alt': "//div[@role='feed']//a[contains(@href, '/maps/place/')]",
    'lugar_link': ".//a[contains(@href, '/maps/place/')]",
    
    # Datos dentro de cada elemento (sin hacer clic)
    'nombre': ".//div[contains(@class, 'qBF1Pd')]",
    'nombre_alt': ".//div[contains(@class, 'fontHeadlineSmall')]",
    'direccion_breve': ".//div[contains(@class, 'W4Efsd')]//span[last()]",
    'direccion_breve_alt': ".//div[contains(@aria-label, 'Dirección') or contains(@aria-label, 'Address')]",
    'rating': ".//span[contains(@class, 'MW4etd')]",
    'num_resenas': ".//span[contains(@class, 'UY7F9')]",
    'categoria': ".//div[contains(@class, 'W4Efsd')]//span[1]",
    
    # Teléfono en la lista (varios selectores posibles)
    'telefono_lista': ".//span[contains(@aria-label, 'Teléfono') or contains(@aria-label, 'Phone')]",
    'telefono_lista_alt': ".//div[contains(text(), '+') or contains(text(), '(')]",
    
    # Botón de consentimiento
    'consent_button': "//button[.//span[contains(text(), 'Aceptar') or contains(text(), 'Accept')]]",
    'consent_button_alt': "//form[@action]//button",
    
    # Detección de fin de resultados
    'mensaje_fin': "//span[contains(text(), 'Has llegado al final') or contains(text(), \"You've reached the end\")]",
}

# Selectores para datos detallados (si se hace clic en un lugar)
DETAIL_SELECTORS = {
    'nombre_completo': "h1[class*='fontHeadline']",
    'direccion_completa': "//button[@data-item-id='address']//div[contains(@class, 'fontBody')]",
    'telefono': "//button[contains(@data-item-id, 'phone')]//div[contains(@class, 'fontBody')]",
    'sitio_web': "//a[@data-item-id='authority']",
    'email': "//a[contains(@href, 'mailto:')]",
    'horarios': "//div[contains(@aria-label, 'Horario')]",
    'rango_precios': "//span[contains(@aria-label, 'Precio')]",
}

# User Agents para rotación
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
]
