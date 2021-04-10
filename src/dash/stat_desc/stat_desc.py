import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from src.dash.app import app
from dash.dependencies import Input, Output
data = pd.read_csv(r'C:\Users\SURFACE\Documents\GitHub\Hackathon-equipe_5\df_petit.csv')
data_churn = data.loc[data.target == 1]
data_cl = data.loc[data.target == 0]
churn_date = data_churn.groupby('date').sum().target

@app.callback(Output("date_churn","figure"),
              [Input("date-range", "start_date"),
               Input("date-range", "end_date")
               ])
def update_charts(start_date, end_date):
    mask=((churn_date.index <= end_date)
            & (churn_date.index >= start_date)
          )
    figure = px.line(
        x=churn_date[mask].index,
        y=churn_date[mask],
        labels=['Nombre de Churn'],
    )
    figure.update_layout(title={
        'text': 'Churn en fonction de la date',
        'font': {'size': 25},
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    return figure

def double_histo(variables, title):
    fig = go.Figure()
    # on ajoute les deux traces
    fig.add_trace(go.Histogram(x=data_churn[variables],
                               name='Churn',
                               histnorm='probability density'))
    fig.add_trace(go.Histogram(x=data_cl[variables],
                               name='Non churn',
                               histnorm='probability density'))

    # on fait en sorte que les histogrammes soient cote à cote
    fig.update_layout(barmode='group', title={
        'text': title,
        'font': {'size': 25},
        'y': 0.9,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    # on set-up l'opacité des histogrammes
    fig.update_traces(opacity=1)
    return (fig)

layout = html.Div(
    children= \
        [html.H1(children="Too Good To Go Analytics", className="header-title"),
         html.P(
             children="Bienvenue ! "
                      "Commencez par choisir un onglet à visiter :",
            className="header-description",
         ),
     html.Div(children=[
         dcc.Graph(
             id="segment_chart",
             figure=double_histo('store_segment',
                                 'Graphique représentants le taux de churn en fonction du segment du magasin')),
         ],
         className='card',
     ),
         html.P(
             children="On peut voir ici les distributions des magasins qui ont churn ou non en fonction des secteurs. On peut observer une distribution différente entre les deux features :"
                      "en efet, on observe que les boulangeries ont moins tendances à faire défection (en effet la probabilité qu'une boulangerie churn, comme on peut le voir dans "
                      "l'histogramme, est plus faible que pour les autrres secteurs). Au contraire, on peut voir que les restaurants traditionnels, ont eux plus tendance à faire défaut"
                      "que d'autres types de magasin, car on observe en proportion plus de restaurant traditionnel dans les magasins qui ont churn que dans les magasins qu'on a pas churn."
                      "Les différences de distribution entre magasin qui ont churn et qui n'ont pas churn peut nous faire penser que celle-ci sera une variable de prédiction intéressante "
                      "pour savoir si un magasin va churn ou non",
             className="description",
         ),
        html.Div(
                    children=[
                        html.Div(
                            children="Date Range",
                            className="menu-title"
                            ),
                        dcc.DatePickerRange(
                            id="date-range",
                            min_date_allowed=churn_date.index.min(),
                            max_date_allowed=churn_date.index.max(),
                            start_date=churn_date.index.min(),
                            end_date=churn_date.index.max(),
                        ),
                    ],
        ),
     html.Div(
         children=[
             dcc.Graph(
                 id="date_churn"
                 )
         ],
         className ='card',
     ),
             html.P(
                 children="On a représenté ici les churns en fonction de la date. Ce graphique met en évidence l'impact très fort qu'a pu avoir les confinements sur le nombre de churn dans les"
                          "mois qui ont suivis. En effet, on passe d'un régime relativement stationnaire et bas au début de la période a un pallier plus élevé au moment du premier confinement "
                          "pour redescendre à la fin de celui-ci. C'est cependant sur la fin de la période que l'on peut observer le plus grand nombre de défection, cela étant probablement du"
                          "encore une fois aux nombreuses restrictions sanitaires, qui ont possiblement plongé de nombreux établissements vers l'inactivités et donc parrallèlement à Churn sur "
                          "Too good to go",
             className="description",
                )
            ],
        )
