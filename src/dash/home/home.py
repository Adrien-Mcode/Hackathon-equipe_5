import dash
import dash_core_components as dcc
import dash_html_components as html
from src.dash.app import app

layout = html.Div(
    children= \
        [html.Img(
            src=app.get_asset_url('favicon.ico'),
            height='40 px',
            width='auto',
            className='header-image'
        ),
         html.H1(children="Too Good To Go Analytics", className="header-title"),
         html.P(
            children=["Bienvenue sur Too Good To Go Analytics !",
                      html.Br(),
                     "Commencez par choisir un onglet à visiter :"],
            className="header-description",       
         )],
    className="header",
)
