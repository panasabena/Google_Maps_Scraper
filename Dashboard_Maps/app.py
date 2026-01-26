"""
Dashboard Principal de Monitoreo de Scraping Argentina
Aplicación desarrollada con Dash y Plotly
"""

import dash
from dash import dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
sys.path.insert(0, os.path.dirname(__file__))

# Importar módulos propios
from src.data_loader import DataLoader
from src.statistics_calculator import StatisticsCalculator
from src.progress_tracker import ProgressTracker
from src.map_generator import MapGenerator
from config import FILE_PATHS, DASHBOARD_CONFIG, PROVINCIAS_ARGENTINA, RUBROS_BUSQUEDA, UBICACIONES_ARGENTINA

# Inicializar la aplicación Dash
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="Dashboard Scraping Argentina"
)

# Inicializar cargadores de datos
data_loader = DataLoader(
    csv_path=FILE_PATHS['csv_data'],
    json_path=FILE_PATHS['estado_json']
)

map_generator = MapGenerator()

# Cargar datos iniciales
print("🚀 Iniciando carga de datos...")
df_empresas = data_loader.cargar_datos()
estado_scraping = data_loader.cargar_estado()

# Inicializar calculadores
stats_calc = StatisticsCalculator(df_empresas) if df_empresas is not None else None
progress_tracker = ProgressTracker(estado_scraping)

# Layout principal
def create_layout():
    """Crea el layout del dashboard."""
    
    # Obtener estadísticas
    overview_stats = stats_calc.get_overview_stats() if stats_calc else {}
    progress_summary = progress_tracker.get_progress_summary()
    
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("🗺️ Dashboard de Monitoreo de Scraping - Argentina", 
                           className="text-white mb-2"),
                    html.P("Visualización en tiempo real del progreso de extracción de Google Maps",
                          className="text-white-50 mb-0")
                ], className="dashboard-header")
            ], width=12)
        ], className="mb-4"),
        
        # Banner de actualización
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Strong("📡 Estado: "),
                        html.Span("Activo", id="status-badge", className="badge badge-success ms-2"),
                        html.Span(f" | Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                                 id="last-update-time", className="ms-3")
                    ], className="update-info"),
                    html.Button("🔄 Actualizar Ahora", id="btn-refresh", className="btn-refresh")
                ], className="update-banner")
            ], width=12)
        ], className="mb-4"),
        
        # Tabs principales
        dbc.Tabs([
            # Tab 1: Resumen General
            dbc.Tab(label="📊 Resumen General", tab_id="tab-overview", children=[
                html.Div([
                    # Cards de estadísticas principales
                    dbc.Row([
                        dbc.Col([
                            create_stat_card(
                                "Total Empresas",
                                f"{overview_stats.get('total_empresas', 0):,}",
                                "📍",
                                "primary"
                            )
                        ], md=3),
                        dbc.Col([
                            create_stat_card(
                                "Progreso General",
                                f"{progress_summary.get('porcentaje_completado', 0)}%",
                                "📈",
                                "success"
                            )
                        ], md=3),
                        dbc.Col([
                            create_stat_card(
                                "Provincias",
                                f"{overview_stats.get('total_provincias', 0)}",
                                "🗺️",
                                "info"
                            )
                        ], md=3),
                        dbc.Col([
                            create_stat_card(
                                "Calidad de Datos",
                                f"{overview_stats.get('calidad_datos', 0)}%",
                                "⭐",
                                "warning"
                            )
                        ], md=3),
                    ], className="mb-4"),
                    
                    # Gráficos de progreso
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                dcc.Graph(id="graph-progress-gauge")
                            ], className="chart-container")
                        ], md=6),
                        dbc.Col([
                            html.Div([
                                dcc.Graph(id="graph-progress-donut")
                            ], className="chart-container")
                        ], md=6),
                    ], className="mb-4"),
                    
                    # Detalles de calidad
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("📋 Calidad de Datos", className="mb-3"),
                                dbc.Row([
                                    dbc.Col([
                                        create_quality_indicator(
                                            "Con Email",
                                            overview_stats.get('con_email', 0),
                                            overview_stats.get('total_empresas', 1),
                                            overview_stats.get('porcentaje_email', 0)
                                        )
                                    ], md=3),
                                    dbc.Col([
                                        create_quality_indicator(
                                            "Con Teléfono",
                                            overview_stats.get('con_telefono', 0),
                                            overview_stats.get('total_empresas', 1),
                                            overview_stats.get('porcentaje_telefono', 0)
                                        )
                                    ], md=3),
                                    dbc.Col([
                                        create_quality_indicator(
                                            "Con Sitio Web",
                                            overview_stats.get('con_web', 0),
                                            overview_stats.get('total_empresas', 1),
                                            overview_stats.get('porcentaje_web', 0)
                                        )
                                    ], md=3),
                                    dbc.Col([
                                        create_quality_indicator(
                                            "Con Rating",
                                            overview_stats.get('con_rating', 0),
                                            overview_stats.get('total_empresas', 1),
                                            overview_stats.get('porcentaje_rating', 0)
                                        )
                                    ], md=3),
                                ])
                            ], className="chart-container")
                        ], width=12)
                    ])
                ], className="mt-4")
            ]),
            
            # Tab 2: Mapa Interactivo
            dbc.Tab(label="🗺️ Mapa Interactivo", tab_id="tab-map", children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("Ubicaciones de Scraping", className="mb-3"),
                                dcc.Graph(id="graph-ubicaciones-map", style={'height': '600px'})
                            ], className="map-container")
                        ], width=12)
                    ], className="mb-4 mt-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("Densidad de Empresas", className="mb-3"),
                                dcc.Dropdown(
                                    id="dropdown-map-type",
                                    options=[
                                        {'label': '🔥 Mapa de Calor', 'value': 'heatmap'},
                                        {'label': '📍 Puntos por Provincia', 'value': 'scatter_provincia'},
                                        {'label': '🏢 Puntos por Categoría', 'value': 'scatter_categoria'},
                                    ],
                                    value='heatmap',
                                    className="mb-3"
                                ),
                                dcc.Graph(id="graph-empresas-map", style={'height': '600px'})
                            ], className="map-container")
                        ], width=12)
                    ])
                ])
            ]),
            
            # Tab 3: Estadísticas Detalladas
            dbc.Tab(label="📈 Estadísticas", tab_id="tab-stats", children=[
                html.Div([
                    # Filtros
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("🔍 Filtros", className="mb-3"),
                                
                                html.Label("Provincias:"),
                                dcc.Dropdown(
                                    id="filter-provincias",
                                    options=[{'label': p, 'value': p} for p in sorted(PROVINCIAS_ARGENTINA)],
                                    multi=True,
                                    placeholder="Todas las provincias",
                                    className="mb-3"
                                ),
                                
                                html.Label("Rubros (top 50):"),
                                dcc.Dropdown(
                                    id="filter-rubros",
                                    options=[{'label': r, 'value': r} for r in RUBROS_BUSQUEDA[:50]],
                                    multi=True,
                                    placeholder="Todos los rubros",
                                    className="mb-3"
                                ),
                                
                                html.Label("Rating mínimo:"),
                                dcc.Slider(
                                    id="filter-rating",
                                    min=0,
                                    max=5,
                                    step=0.5,
                                    value=0,
                                    marks={i: str(i) for i in range(6)},
                                    className="mb-3"
                                ),
                                
                                dbc.Checklist(
                                    id="filter-calidad",
                                    options=[
                                        {'label': ' Con Email', 'value': 'email'},
                                        {'label': ' Con Teléfono', 'value': 'telefono'},
                                        {'label': ' Con Sitio Web', 'value': 'web'},
                                    ],
                                    value=[],
                                    className="mb-3"
                                ),
                                
                                html.Button("Aplicar Filtros", id="btn-apply-filters", 
                                          className="btn btn-primary w-100")
                            ], className="filters-sidebar")
                        ], md=3),
                        
                        # Gráficos de estadísticas
                        dbc.Col([
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dcc.Graph(id="graph-top-provincias")
                                    ], className="chart-container")
                                ], md=6),
                                dbc.Col([
                                    html.Div([
                                        dcc.Graph(id="graph-top-categorias")
                                    ], className="chart-container")
                                ], md=6),
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dcc.Graph(id="graph-timeline")
                                    ], className="chart-container")
                                ], width=12)
                            ]),
                            dbc.Row([
                                dbc.Col([
                                    html.Div([
                                        dcc.Graph(id="graph-rating-distribution")
                                    ], className="chart-container")
                                ], width=12)
                            ])
                        ], md=9)
                    ], className="mt-4")
                ])
            ]),
            
            # Tab 4: Progreso de Scraping
            dbc.Tab(label="⚙️ Progreso", tab_id="tab-progress", children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("📊 Progreso por Provincia", className="mb-3"),
                                dcc.Graph(id="graph-progress-provincias")
                            ], className="chart-container")
                        ], width=12)
                    ], className="mb-4 mt-4"),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("📍 Estado de Ubicaciones", className="mb-3"),
                                html.Div(id="table-ubicaciones-status")
                            ], className="chart-container")
                        ], width=12)
                    ])
                ])
            ]),
            
            # Tab 5: Datos
            dbc.Tab(label="📄 Datos", tab_id="tab-data", children=[
                html.Div([
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.H3("🔍 Búsqueda de Empresas", className="mb-3"),
                                dbc.Input(
                                    id="search-empresas",
                                    type="text",
                                    placeholder="Buscar por nombre, ciudad o categoría...",
                                    className="mb-3"
                                ),
                                html.Div(id="table-empresas-container")
                            ], className="chart-container")
                        ], width=12)
                    ], className="mt-4")
                ])
            ]),
        ], id="tabs-main", active_tab="tab-overview"),
        
        # Store para datos filtrados
        dcc.Store(id='store-filtered-data'),
        
        # Interval para actualización automática
        dcc.Interval(
            id='interval-component',
            interval=DASHBOARD_CONFIG['update_interval'] * 1000,  # en milisegundos
            n_intervals=0
        )
        
    ], fluid=True, className="dashboard-container")

def create_stat_card(title, value, icon, color_class="primary"):
    """Crea una card de estadística."""
    return html.Div([
        html.H3(title, className="mb-2"),
        html.Div([
            html.Span(value, className="stat-value"),
            html.Span(icon, className="stat-icon")
        ], style={'position': 'relative'})
    ], className=f"stats-card {color_class}")

def create_quality_indicator(label, value, total, percentage):
    """Crea un indicador de calidad."""
    return html.Div([
        html.H5(label, className="mb-2"),
        html.H3(f"{value:,}", className="text-primary mb-1"),
        html.Div([
            html.Div(
                style={
                    'width': f'{percentage}%',
                    'height': '8px',
                    'background': 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                    'border-radius': '4px',
                    'transition': 'width 0.5s'
                }
            )
        ], style={
            'width': '100%',
            'height': '8px',
            'background': '#e9ecef',
            'border-radius': '4px',
            'margin-bottom': '5px'
        }),
        html.Small(f"{percentage}% del total", className="text-muted")
    ])

# Asignar layout
app.layout = create_layout()

# Callbacks

@app.callback(
    [Output('graph-progress-gauge', 'figure'),
     Output('graph-progress-donut', 'figure'),
     Output('last-update-time', 'children')],
    [Input('btn-refresh', 'n_clicks'),
     Input('interval-component', 'n_intervals')]
)
def update_progress_graphs(n_clicks, n_intervals):
    """Actualiza los gráficos de progreso."""
    # Recargar datos si es necesario
    csv_cambio, json_cambio = data_loader.necesita_actualizacion()
    
    if csv_cambio or json_cambio:
        global df_empresas, estado_scraping, stats_calc, progress_tracker
        if csv_cambio:
            df_empresas = data_loader.cargar_datos(force_reload=True)
            stats_calc = StatisticsCalculator(df_empresas)
        if json_cambio:
            estado_scraping = data_loader.cargar_estado(force_reload=True)
            progress_tracker = ProgressTracker(estado_scraping)
    
    progress_summary = progress_tracker.get_progress_summary()
    
    # Gauge
    gauge_fig = map_generator.create_progress_gauge(
        progress_summary.get('porcentaje_completado', 0),
        "Progreso General"
    )
    
    # Donut
    donut_fig = map_generator.create_progress_donut(
        progress_summary.get('combinaciones_completadas', 0),
        progress_summary.get('combinaciones_pendientes', 0)
    )
    
    update_time = f" | Última actualización: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    return gauge_fig, donut_fig, update_time

@app.callback(
    Output('graph-ubicaciones-map', 'figure'),
    [Input('btn-refresh', 'n_clicks')]
)
def update_ubicaciones_map(n_clicks):
    """Actualiza el mapa de ubicaciones con empresas como puntos."""
    ubicaciones_status = progress_tracker.get_ubicaciones_status()
    return map_generator.create_ubicaciones_map(ubicaciones_status, df_empresas)

@app.callback(
    Output('graph-empresas-map', 'figure'),
    [Input('dropdown-map-type', 'value'),
     Input('store-filtered-data', 'data')]
)
def update_empresas_map(map_type, filtered_data):
    """Actualiza el mapa de empresas."""
    df = df_empresas if filtered_data is None else pd.DataFrame(filtered_data)
    
    if map_type == 'heatmap':
        return map_generator.create_heatmap(df)
    elif map_type == 'scatter_provincia':
        return map_generator.create_scatter_map(df, 'provincia')
    elif map_type == 'scatter_categoria':
        return map_generator.create_scatter_map(df, 'categoria')
    else:
        return map_generator.create_heatmap(df)

@app.callback(
    Output('store-filtered-data', 'data'),
    [Input('btn-apply-filters', 'n_clicks')],
    [State('filter-provincias', 'value'),
     State('filter-rubros', 'value'),
     State('filter-rating', 'value'),
     State('filter-calidad', 'value')]
)
def apply_filters(n_clicks, provincias, rubros, min_rating, calidad):
    """Aplica los filtros seleccionados."""
    if n_clicks is None:
        return None
    
    df_filtrado = data_loader.filtrar_datos(
        provincias=provincias,
        rubros=rubros,
        min_rating=min_rating,
        tiene_email='email' in calidad if calidad else None,
        tiene_telefono='telefono' in calidad if calidad else None,
        tiene_web='web' in calidad if calidad else None
    )
    
    return df_filtrado.to_dict('records') if len(df_filtrado) > 0 else None

@app.callback(
    [Output('graph-top-provincias', 'figure'),
     Output('graph-top-categorias', 'figure'),
     Output('graph-timeline', 'figure'),
     Output('graph-rating-distribution', 'figure')],
    [Input('store-filtered-data', 'data')]
)
def update_stats_graphs(filtered_data):
    """Actualiza los gráficos de estadísticas."""
    df = df_empresas if filtered_data is None else pd.DataFrame(filtered_data)
    calc = StatisticsCalculator(df)
    
    # Top provincias
    provincia_stats = calc.get_distribution_by_province()
    fig_provincias = go.Figure(data=[
        go.Bar(x=provincia_stats['total_empresas'][:10], 
               y=provincia_stats['provincia'][:10],
               orientation='h',
               marker_color='steelblue')
    ])
    fig_provincias.update_layout(title="Top 10 Provincias", xaxis_title="Empresas", yaxis_title="")
    
    # Top categorías
    categoria_stats = calc.get_distribution_by_category(top_n=15)
    fig_categorias = go.Figure(data=[
        go.Bar(x=categoria_stats['categoria'], 
               y=categoria_stats['total'],
               marker_color='coral')
    ])
    fig_categorias.update_layout(title="Top 15 Categorías", xaxis_title="", yaxis_title="Empresas")
    fig_categorias.update_xaxes(tickangle=-45)
    
    # Timeline
    timeline_data = calc.get_timeline_data('dia')
    fig_timeline = go.Figure()
    if len(timeline_data) > 0:
        fig_timeline.add_trace(go.Scatter(x=timeline_data['fecha'], y=timeline_data['total_empresas'],
                                         mode='lines+markers', name='Diario'))
        fig_timeline.add_trace(go.Scatter(x=timeline_data['fecha'], y=timeline_data['acumulado'],
                                         mode='lines', name='Acumulado'))
    fig_timeline.update_layout(title="Empresas Extraídas por Día", xaxis_title="Fecha", yaxis_title="Empresas")
    
    # Distribución de ratings
    rating_dist = calc.get_rating_distribution()
    fig_rating = go.Figure()
    if rating_dist:
        fig_rating.add_trace(go.Bar(x=rating_dist['rangos'], y=rating_dist['conteos'],
                                    marker_color='lightseagreen'))
    fig_rating.update_layout(title="Distribución de Ratings", xaxis_title="Rating", yaxis_title="Cantidad")
    
    return fig_provincias, fig_categorias, fig_timeline, fig_rating

@app.callback(
    Output('graph-progress-provincias', 'figure'),
    [Input('btn-refresh', 'n_clicks')]
)
def update_progress_provincias(n_clicks):
    """Actualiza el gráfico de progreso por provincia."""
    provincias_progress = progress_tracker.get_provincias_progress()
    return map_generator.create_progress_bar_chart(provincias_progress)

@app.callback(
    Output('table-ubicaciones-status', 'children'),
    [Input('btn-refresh', 'n_clicks')]
)
def update_ubicaciones_table(n_clicks):
    """Actualiza la tabla de estado de ubicaciones."""
    ubicaciones_status = progress_tracker.get_ubicaciones_status()
    
    if not ubicaciones_status:
        return html.P("No hay datos disponibles")
    
    df_status = pd.DataFrame(ubicaciones_status)
    df_status = df_status[['nombre', 'provincia', 'estado', 'rubros_completados', 'total_rubros', 'porcentaje_completado']]
    
    return dash_table.DataTable(
        data=df_status.to_dict('records'),
        columns=[
            {'name': 'Ubicación', 'id': 'nombre'},
            {'name': 'Provincia', 'id': 'provincia'},
            {'name': 'Estado', 'id': 'estado'},
            {'name': 'Rubros', 'id': 'rubros_completados'},
            {'name': 'Total', 'id': 'total_rubros'},
            {'name': 'Progreso %', 'id': 'porcentaje_completado'},
        ],
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'backgroundColor': '#667eea', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'filter_query': '{estado} = completed'}, 'backgroundColor': '#d4edda'},
            {'if': {'filter_query': '{estado} = partial'}, 'backgroundColor': '#fff3cd'},
            {'if': {'filter_query': '{estado} = pending'}, 'backgroundColor': '#f8d7da'},
        ],
        page_size=20,
        sort_action='native',
        filter_action='native'
    )

@app.callback(
    Output('table-empresas-container', 'children'),
    [Input('search-empresas', 'value'),
     Input('store-filtered-data', 'data')]
)
def update_empresas_table(search_value, filtered_data):
    """Actualiza la tabla de empresas."""
    df = df_empresas if filtered_data is None else pd.DataFrame(filtered_data)
    
    if df is None or len(df) == 0:
        return html.P("No hay datos disponibles")
    
    # Aplicar búsqueda
    if search_value:
        mask = (
            df['nombre'].str.contains(search_value, case=False, na=False) |
            df['ciudad'].str.contains(search_value, case=False, na=False) |
            df['categoria'].str.contains(search_value, case=False, na=False)
        )
        df = df[mask]
    
    # Limitar columnas
    cols = ['nombre', 'ciudad', 'provincia', 'categoria', 'rating', 'telefono', 'email', 'sitio_web']
    df_display = df[[col for col in cols if col in df.columns]].head(100)
    
    return dash_table.DataTable(
        data=df_display.to_dict('records'),
        columns=[{'name': col.capitalize(), 'id': col} for col in df_display.columns],
        style_cell={'textAlign': 'left', 'padding': '10px', 'maxWidth': '200px', 'overflow': 'hidden'},
        style_header={'backgroundColor': '#667eea', 'color': 'white', 'fontWeight': 'bold'},
        style_data_conditional=[
            {'if': {'row_index': 'odd'}, 'backgroundColor': '#f8f9fa'}
        ],
        page_size=50,
        sort_action='native',
        filter_action='native',
        export_format='csv'
    )

# Ejecutar la aplicación
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 Dashboard de Monitoreo de Scraping Argentina")
    print("="*60)
    print(f"📊 Empresas cargadas: {len(df_empresas):,}" if df_empresas is not None else "⚠️  Sin datos")
    print(f"📍 Ubicaciones configuradas: {len(UBICACIONES_ARGENTINA)}")
    print(f"🏷️  Rubros configurados: {len(RUBROS_BUSQUEDA)}")
    print(f"🌐 Servidor iniciando en http://localhost:{DASHBOARD_CONFIG['port']}/")
    print("="*60 + "\n")
    
    app.run(
        debug=DASHBOARD_CONFIG['debug'],
        port=DASHBOARD_CONFIG['port'],
        host='127.0.0.1'
    )
