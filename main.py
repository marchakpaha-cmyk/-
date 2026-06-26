import dash
from dash import dcc, html, Input, Output, State
import dash_leaflet as dl
from transport_data import TRANSPORT_DB

app = dash.Dash(__name__)
server = app.server

# Стили 
METRO_COLORS = {'bg': '#111111', 'surface': '#252525', 'accent': '#00ff00'}

app.layout = html.Div(style={'fontFamily': 'sans-serif'}, children=[
    html.Button("МЕНЮ", id="burger-btn", n_clicks=0, style={
        'position': 'absolute', 'top': '15px', 'left': '15px',
        'backgroundColor': METRO_COLORS['accent'], 'padding': '10px 15px'
    }),
    html.Div(id="sidebar", style={'position': 'absolute', 'top': '0', 'left': '-300px', 'width': '300px', 'backgroundColor': METRO_COLORS['surface'], 'height': '100%'}, children=[
        html.H3("МАРШРУТЫ", style={'color': 'white', 'padding': '20px'}),
    ])
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)
