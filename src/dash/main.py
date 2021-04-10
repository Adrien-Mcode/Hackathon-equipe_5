import dash_core_components as dcc
import dash_html_components as html
import src.dash.home.home as home
import src.dash.model_report.model_report as model_report
import src.dash.stat_desc.stat_desc as stat_desc
from dash.dependencies import Input, Output
from src.dash.app import app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(children="Menu Principal", className="menu-title"),
    dcc.Dropdown(
        id="menu-principal",
        options=[
            {"label": region, "value": region}
            for region in ["statistiques_descriptives", "model_report"]
        ],
        value="linear_regression",
        clearable=False,
        className="menu-box",
    ),
    html.Div(id='page-content')
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/statistiques_descriptives':
        return stat_desc.layout
    elif pathname == '/model_report':
        return model_report.layout
    else:
        return home.layout


@app.callback(Output('url', 'pathname'),
              [Input("menu-principal", "value")])
def display_page(pathname):
    return f'/{pathname}'


if __name__ == '__main__':
    app.run_server(debug=True)
