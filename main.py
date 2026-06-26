import dash
from dash import html
from transport_data import TRANSPORT_DB

app = dash.Dash(__name__)
server = app.server

app.layout = html.Div([
    html.H1("Карта транспорта Киева"),
    html.Div(f"Всего маршрутов: {len(TRANSPORT_DB.get('Киев', {}))}")
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=10000)
