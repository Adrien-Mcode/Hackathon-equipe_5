import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from src.dash.tabs import tab_1, tab_2
import numpy as np

print(dcc.__version__)  # 0.6.0 or above is required




app.layout = html.Div([
    # represents the URL bar, doesn't render anything
    dcc.Location(id='url', refresh=False),
    html.Div(children="Region", className="menu-title"),
        dcc.Dropdown(
            id="region-filter",
            options=[
                {"label": region, "value": region}
                for region in ["linear_regression", "random_forest"]
            ],
            value="linear_regression",
            clearable=False,
            className="dropdown",
        ),

    # content will be rendered in this element
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    return html.Div([
        html.H3('You are on page {}'.format(pathname))
    ])


@app.callback(Output('url', 'pathname'),
              [Input('region-filter', 'value')])
def display_page(model_name):
    return f"/{model_name}"


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return tab_1.tab_1_layout
    elif tab == 'tab-2-example':
        return tab_2.tab_2_layout


# Tab 1 callback
@app.callback(Output('page-1-content', 'children'),
              [Input('page-1-dropdown', 'value')])
def page_1_dropdown(value):
    return 'You have selected "{}"'.format(value)


# Tab 2 callback
@app.callback(Output('page-2-content', 'children'),
              [Input('page-2-radios', 'value')])
def page_2_radios(value):
    return 'You have selected "{}"'.format(value)




@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/statistiques_descriptives':
        return stat_desc.layout
    elif pathname == '/model_report':
        return model_report.layout
    else:
        return home.layout

@app.callback(dash.dependencies.Output('url', 'pathname'),
              [Input("region-filter", "value")])
def display_page(pathname):
    return f'/{pathname}'

if __name__ == '__main__':
    app.run_server(debug=True)
