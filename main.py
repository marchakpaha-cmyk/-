import dash
from dash import dcc, html, Input, Output, State
import dash_leaflet as dl
from transport_data import TRANSPORT_DB

app = dash.Dash(__name__)
server = app.server  # <--- ВОТ ЭТУ СТРОКУ ДОБАВЬ

# ... далее весь твой старый код ...

# Стили в духе Metro UI
METRO_COLORS = {'bg': '#111111', 'surface': '#252525', 'accent': '#0078D7', 'text': '#FFFFFF'}

app.layout = html.Div(style={'fontFamily': '"Segoe UI", sans-serif', 'backgroundColor': METRO_COLORS['bg'], 'color': METRO_COLORS['text'], 'height': '100vh', 'margin': '0', 'overflow': 'hidden', 'position': 'relative'}, children=[
    
    # Кнопка Бургер-меню
    html.Button("☰ МЕНЮ", id="burger-btn", n_clicks=0, style={
        'position': 'absolute', 'top': '15px', 'left': '15px', 'zIndex': '1000',
        'backgroundColor': METRO_COLORS['accent'], 'color': 'white', 'border': 'none',
        'padding': '10px 15px', 'fontSize': '16px', 'cursor': 'pointer', 'boxShadow': '0 4px 6px rgba(0,0,0,0.3)'
    }),

    # Выдвижная боковая панель (Бургер-меню)
    html.Div(id="sidebar", style={
        'position': 'absolute', 'top': '0', 'left': '-350px', 'width': '300px', 'height': '100vh',
        'backgroundColor': METRO_COLORS['surface'], 'zIndex': '999', 'padding': '60px 20px 20px',
        'transition': 'left 0.3s ease', 'boxShadow': '2px 0 10px rgba(0,0,0,0.5)'
    }, children=[
        html.H3("МАРШРУТЫ", style={'fontWeight': '300', 'marginBottom': '20px'}),
        html.Label("Город:"),
        dcc.Dropdown(id='city-picker', options=[{'label': c, 'value': c} for c in TRANSPORT_DB.keys()], value='Киев', style={'color': '#000', 'marginBottom': '15px'}),
        html.Label("Вид транспорта:"),
        dcc.Dropdown(id='type-picker', style={'color': '#000', 'marginBottom': '15px'}),
        html.Label("Линия:"),
        dcc.Dropdown(id='line-picker', style={'color': '#000', 'marginBottom': '20px'}),
        html.Button("ПОКАЗАТЬ МАРШРУТ", id="show-route-btn", n_clicks=0, style={
            'width': '100%', 'backgroundColor': METRO_COLORS['accent'], 'color': 'white',
            'border': 'none', 'padding': '12px', 'fontSize': '16px', 'cursor': 'pointer'
        })
    ]),

    # Карта (Спутник)
    html.Div(style={'width': '100vw', 'height': '100vh', 'position': 'absolute', 'top': '0', 'left': '0', 'zIndex': '1'}, children=[
        dl.Map(center=[50.4501, 30.5234], zoom=12, zoomControl=False, children=[
            # Слой спутниковой карты Esri World Imagery
            dl.TileLayer(url="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"),
            dl.LayerGroup(id="map-layers")
        ], style={'width': '100%', 'height': '100%'})
    ])
])

# Логика выдвижения меню
@app.callback(Output("sidebar", "style"), Input("burger-btn", "n_clicks"), State("sidebar", "style"))
def toggle_sidebar(n_clicks, style):
    if n_clicks % 2 == 1:
        style['left'] = '0px'
    else:
        style['left'] = '-350px'
    return style

# Обновление выпадающих списков
@app.callback(Output('type-picker', 'options'), Input('city-picker', 'value'))
def set_types(city):
    return [{'label': t, 'value': t} for t in TRANSPORT_DB[city].keys()] if city else []

@app.callback(Output('line-picker', 'options'), Input('city-picker', 'value'), Input('type-picker', 'value'))
def set_lines(city, t_type):
    return [{'label': l, 'value': l} for l in TRANSPORT_DB[city][t_type].keys()] if city and t_type else []

# Отрисовка маршрута по кнопке
@app.callback(
    Output('map-layers', 'children'),
    Input('show-route-btn', 'n_clicks'),
    State('city-picker', 'value'), State('type-picker', 'value'), State('line-picker', 'value')
)
def update_map(n_clicks, city, t_type, line):
    if n_clicks == 0 or not city or not t_type or not line: return []
    data = TRANSPORT_DB[city][t_type][line]
    elements, points = [], []
    
    for s_name, s_data in data['stations'].items():
        coords = s_data['coords']
        if coords == [0, 0]: continue # Пропускаем станции без координат
        points.append(coords)
        opacity = 0.5 if data.get('status') in ['historical', 'project'] else 1.0
        elements.append(dl.CircleMarker(
            center=coords, radius=5, color=data['color'], fill=True, fillOpacity=opacity,
            children=[dl.Tooltip(s_name)]
        ))
    if len(points) > 1:
        elements.append(dl.Polyline(positions=points, color=data['color'], weight=4))
    return elements

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
