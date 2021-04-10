import dash
import dash_core_components as dcc
import dash_html_components as html
from src.dash.app import app


layout = html.Div(
    children= \
        [html.H1(children="Too Good To Go Analytics", className="header-title"),
         html.P(
             children="Bienvenue ! "
                      "Commencez par choisir un onglet à visiter :",
            className="header-description",   
         )
         ],
    className="header",
)
