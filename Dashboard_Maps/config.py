"""
Configuración del Dashboard de Monitoreo de Scraping Argentina
Contiene ubicaciones, rubros y parámetros de configuración
"""

import os

# Obtener ruta base del proyecto
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Dashboard_Maps/
PARENT_DIR = os.path.dirname(BASE_DIR)  # Scraper_Maps/

# Ubicaciones de Argentina (28 ciudades principales)
UBICACIONES_ARGENTINA = {
    # Ciudad Autónoma de Buenos Aires
    "buenos_aires_argentina": {
        "nombre": "Buenos Aires, Argentina",
        "provincia": "Ciudad Autónoma de Buenos Aires",
        "lat": -34.6037,
        "lng": -58.3816
    },
    
    # Provincia de Buenos Aires
    "la_plata_argentina": {
        "nombre": "La Plata, Argentina",
        "provincia": "Buenos Aires",
        "lat": -34.9215,
        "lng": -57.9545
    },
    "mar_del_plata_argentina": {
        "nombre": "Mar del Plata, Argentina",
        "provincia": "Buenos Aires",
        "lat": -38.0055,
        "lng": -57.5426
    },
    "bahia_blanca_argentina": {
        "nombre": "Bahía Blanca, Argentina",
        "provincia": "Buenos Aires",
        "lat": -38.7183,
        "lng": -62.2663
    },
    
    # Córdoba
    "córdoba_argentina": {
        "nombre": "Córdoba, Argentina",
        "provincia": "Córdoba",
        "lat": -31.4201,
        "lng": -64.1888
    },
    "rio_cuarto_argentina": {
        "nombre": "Río Cuarto, Argentina",
        "provincia": "Córdoba",
        "lat": -33.1301,
        "lng": -64.3495
    },
    
    # Santa Fe
    "rosario_argentina": {
        "nombre": "Rosario, Argentina",
        "provincia": "Santa Fe",
        "lat": -32.9468,
        "lng": -60.6393
    },
    "santa_fe_argentina": {
        "nombre": "Santa Fe, Argentina",
        "provincia": "Santa Fe",
        "lat": -31.6333,
        "lng": -60.7000
    },
    
    # Mendoza
    "mendoza_argentina": {
        "nombre": "Mendoza, Argentina",
        "provincia": "Mendoza",
        "lat": -32.8895,
        "lng": -68.8458
    },
    
    # Tucumán
    "san_miguel_de_tucuman_argentina": {
        "nombre": "San Miguel de Tucumán, Argentina",
        "provincia": "Tucumán",
        "lat": -26.8083,
        "lng": -65.2176
    },
    
    # Salta
    "salta_argentina": {
        "nombre": "Salta, Argentina",
        "provincia": "Salta",
        "lat": -24.7821,
        "lng": -65.4232
    },
    
    # Entre Ríos
    "parana_argentina": {
        "nombre": "Paraná, Argentina",
        "provincia": "Entre Ríos",
        "lat": -31.7333,
        "lng": -60.5297
    },
    
    # Misiones
    "posadas_argentina": {
        "nombre": "Posadas, Argentina",
        "provincia": "Misiones",
        "lat": -27.3671,
        "lng": -55.8969
    },
    
    # Chaco
    "resistencia_argentina": {
        "nombre": "Resistencia, Argentina",
        "provincia": "Chaco",
        "lat": -27.4514,
        "lng": -58.9867
    },
    
    # Corrientes
    "corrientes_argentina": {
        "nombre": "Corrientes, Argentina",
        "provincia": "Corrientes",
        "lat": -27.4692,
        "lng": -58.8306
    },
    
    # Santiago del Estero
    "santiago_del_estero_argentina": {
        "nombre": "Santiago del Estero, Argentina",
        "provincia": "Santiago del Estero",
        "lat": -27.7834,
        "lng": -64.2642
    },
    
    # Jujuy
    "san_salvador_de_jujuy_argentina": {
        "nombre": "San Salvador de Jujuy, Argentina",
        "provincia": "Jujuy",
        "lat": -24.1858,
        "lng": -65.2995
    },
    
    # Formosa
    "formosa_argentina": {
        "nombre": "Formosa, Argentina",
        "provincia": "Formosa",
        "lat": -26.1775,
        "lng": -58.1781
    },
    
    # Neuquén
    "neuquen_argentina": {
        "nombre": "Neuquén, Argentina",
        "provincia": "Neuquén",
        "lat": -38.9516,
        "lng": -68.0591
    },
    
    # Río Negro
    "viedma_argentina": {
        "nombre": "Viedma, Argentina",
        "provincia": "Río Negro",
        "lat": -40.8135,
        "lng": -62.9967
    },
    
    # Chubut
    "rawson_argentina": {
        "nombre": "Rawson, Argentina",
        "provincia": "Chubut",
        "lat": -43.3002,
        "lng": -65.1023
    },
    
    # Santa Cruz
    "rio_gallegos_argentina": {
        "nombre": "Río Gallegos, Argentina",
        "provincia": "Santa Cruz",
        "lat": -51.6226,
        "lng": -69.2181
    },
    
    # Tierra del Fuego
    "ushuaia_argentina": {
        "nombre": "Ushuaia, Argentina",
        "provincia": "Tierra del Fuego",
        "lat": -54.8019,
        "lng": -68.3029
    },
    
    # San Luis
    "san_luis_argentina": {
        "nombre": "San Luis, Argentina",
        "provincia": "San Luis",
        "lat": -33.2950,
        "lng": -66.3356
    },
    
    # San Juan
    "san_juan_argentina": {
        "nombre": "San Juan, Argentina",
        "provincia": "San Juan",
        "lat": -31.5375,
        "lng": -68.5364
    },
    
    # Catamarca
    "san_fernando_del_valle_de_catamarca_argentina": {
        "nombre": "San Fernando del Valle de Catamarca, Argentina",
        "provincia": "Catamarca",
        "lat": -28.4696,
        "lng": -65.7795
    },
    
    # La Rioja
    "la_rioja_argentina": {
        "nombre": "La Rioja, Argentina",
        "provincia": "La Rioja",
        "lat": -29.4131,
        "lng": -66.8558
    },
    
    # La Pampa
    "santa_rosa_argentina": {
        "nombre": "Santa Rosa, Argentina",
        "provincia": "La Pampa",
        "lat": -36.6167,
        "lng": -64.2833
    }
}

# Rubros de búsqueda - SINCRONIZADO CON EL SCRAPER (198 rubros únicos, sin duplicados)
# Esta lista se limpia automáticamente al final para remover duplicados
_RUBROS_RAW = [
    "fabrica",
    "logistica", 
    "transportes",
    "mudanzas",
    "fletes",
    "agencia de marketing",
    "higiene y seguridad",
    "auditores",
    "cadetería",
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
]

# Remover duplicados manteniendo el orden original
RUBROS_BUSQUEDA = list(dict.fromkeys(_RUBROS_RAW))

print(f"📋 Rubros originales: {len(_RUBROS_RAW)}")
print(f"✅ Rubros únicos: {len(RUBROS_BUSQUEDA)}")
if len(_RUBROS_RAW) != len(RUBROS_BUSQUEDA):
    duplicados = len(_RUBROS_RAW) - len(RUBROS_BUSQUEDA)
    print(f"⚠️  Se encontraron {duplicados} rubros duplicados y fueron removidos")

# Configuración del Dashboard
DASHBOARD_CONFIG = {
    # Actualización automática
    'update_interval': 300,  # segundos (5 minutos)
    
    # Estilo de mapa
    'map_style': 'openstreetmap',  # 'openstreetmap', 'cartodb positron', 'stamen terrain'
    'map_center': [-38.4161, -63.6167],  # Centro de Argentina
    'map_zoom': 5,
    
    # Filtros por defecto
    'default_filters': {
        'min_rating': 0.0,
        'must_have_email': False,
        'must_have_phone': False,
        'must_have_website': False
    },
    
    # Exportación
    'export_options': {
        'max_rows_per_export': 100000,
        'formats': ['csv', 'excel', 'json']
    },
    
    # Colores para estados de procesamiento
    'status_colors': {
        'completed': '#28a745',  # Verde
        'partial': '#ffc107',    # Amarillo
        'pending': '#dc3545'     # Rojo
    },
    
    # Clustering en mapa
    'cluster_max_zoom': 15,
    'cluster_radius': 50,
    
    # Paginación
    'rows_per_page': 50,
    
    # Puerto del servidor
    'port': 8050,
    'debug': False
}

# Rutas de archivos (rutas relativas - funcionan en cualquier computadora)
FILE_PATHS = {
    'csv_data': os.path.join(PARENT_DIR, 'resultados', 'google_maps_results.csv'),
    'estado_json': os.path.join(PARENT_DIR, 'estado_ejecucion.json'),
    'geojson_provincias': os.path.join(BASE_DIR, 'data', 'geo', 'argentina_provincias.geojson'),
    'geojson_departamentos': os.path.join(BASE_DIR, 'data', 'geo', 'argentina_departamentos.geojson'),
    'logs': os.path.join(BASE_DIR, 'logs', 'dashboard.log')
}

# Columnas esperadas en el CSV
CSV_COLUMNS = [
    'nombre', 'direccion', 'ciudad', 'categoria', 'rating', 'num_resenas',
    'telefono', 'sitio_web', 'email', 'url_google_maps', 'latitud', 'longitud',
    'rubro_buscado', 'segmento_id', 'segmento_centro', 'fecha_extraccion'
]

# Provincias de Argentina (para agrupación)
PROVINCIAS_ARGENTINA = [
    "Buenos Aires", "Ciudad Autónoma de Buenos Aires", "Catamarca", "Chaco",
    "Chubut", "Córdoba", "Corrientes", "Entre Ríos", "Formosa", "Jujuy",
    "La Pampa", "La Rioja", "Mendoza", "Misiones", "Neuquén", "Río Negro",
    "Salta", "San Juan", "San Luis", "Santa Cruz", "Santa Fe",
    "Santiago del Estero", "Tierra del Fuego", "Tucumán"
]

# Mapeo de colores para categorías (top categorías)
CATEGORIA_COLORES = {
    'fabrica': '#FF6B6B',
    'logistica': '#4ECDC4',
    'restaurante': '#45B7D1',
    'hotel': '#FFA07A',
    'comercio': '#98D8C8',
    'servicios': '#F7DC6F',
    'salud': '#BB8FCE',
    'educacion': '#85C1E2',
    'construccion': '#F8B739',
    'default': '#95A5A6'
}

def get_total_combinaciones():
    """Calcula el total de combinaciones ubicación × rubro"""
    return len(UBICACIONES_ARGENTINA) * len(RUBROS_BUSQUEDA)

def get_ubicacion_info(ubicacion_key):
    """Obtiene información de una ubicación por su clave"""
    return UBICACIONES_ARGENTINA.get(ubicacion_key, None)

def get_provincia_ubicaciones(provincia):
    """Obtiene todas las ubicaciones de una provincia"""
    return {k: v for k, v in UBICACIONES_ARGENTINA.items() if v['provincia'] == provincia}
