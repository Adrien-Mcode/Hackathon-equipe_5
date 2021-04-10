import dash
import dash_core_components as dcc
import dash_html_components as html
from src.dash.app import app

layout = html.Div(
    children= \
        [html.H1(children="Too Good To Go Analytics", ),
         html.P(
             children="Bienvenue sur Too Good To Go Analytics ! "
                      "Commencez par choisir un onglet à visiter :",
         ),
         dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
             dcc.Tab(label='Explicabilité globale', value='explicabilite-globale'),
             dcc.Tab(label='Explicabilité locale', value='explicabilite-locale'),
             dcc.Tab(label='Performances globales', value='performances-globales')
         ]),
         html.Div(id='tabs-content-example'),
         ]
)
