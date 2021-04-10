import dash
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from src.dash.app import app
from dash.dependencies import Input, Output
import plotly.express as px
from src.dash.model_report.shap_values import shap_layout

df_score = pd.read_csv(r'..\..\df_petit.csv')

@app.callback(Output('scatter_plot_score','figure'),
              [
                  Input('Checklist_type','value'),
                  Input('Checklist_model','value'),
                  Input('Checklist_sample_size','value'),
                  Input('Checklist_only_quanti','value'),
                  Input('Checklist_inputer','value'),
                  Input('selec_metrique_1','value'),
                  Input('selec_metrique_2','value')
              ])
def figure_score (type,model,sample_size,only_quanti,inputer,metric_1,metric_2):
    df = df_score[(df_score.type.isin(type)) &
                  (df_score.model.isin(model)) &
                  (df_score.sample_size.isin(sample_size)) &
                  (df_score.only_quantitative.isin(only_quanti)) &
                  (df_score.inputer.isin(inputer))]
    fig = px.scatter(df,x = str(metric_1),y = str(metric_2))
    fig.update_layout(title={
        'text': 'représentation des modèles en fonction des métriques et variables choisies',
        'font': {'size': 25},
        'y': 0.95,
        'x': 0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    return fig


@app.callback(Output("tabs-content-example", "children"),
              Input("tabs-example", "value"))
def update_children(value):
    if value == 'explicabilite-locale':
        children = shap_layout
        return children
    elif value == 'performances-globales':
        children = [dcc.Dropdown(
            id="selec_metrique_1",
            options=[
                {"label": colonne,
                 "value": colonne} for colonne in ['balanced_accuracy_score',
                                                   'recall_score',
                                                   'precision_score',
                                                   'f1_score',
                                                   'accuracy_score']
        ],
        value="balanced_accuracy_score",
        clearable=False,
        className="menu-box",
    ),
        dcc.Dropdown(
                id="selec_metrique_2",
                options=[
                    {"label": colonne,
                     "value": colonne} for colonne in ['balanced_accuracy_score',
                                                       'recall_score',
                                                       'precision_score',
                                                       'f1_score',
                                                       'accuracy_score']
                ],
                value="recall_score",
                clearable=False,
                className="menu-box",
            ),
            dcc.Checklist(
                id="Checklist_type",
                options=[
                    {'label': 'type = test', 'value': 'test'},
                    {'label': 'type = train', 'value': 'train'},
                ],
                value=['test','train'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id="Checklist_model",
                options=[
                    {'label': 'model = lightgbm', 'value': 'lightgbm'},
                    {'label': 'model = logit', 'value': 'logit'},
                    {'label': 'model = rfc', 'value': 'rfc'}
                ],
                value=['lightgbm','logit','rfc'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Checklist(
                id="Checklist_sample_size",
                options=[
                    {'label': 'sample_size = 100000', 'value': 100000},
                    {'label': 'sample_size = 10000', 'value': 10000},
                    {'label': 'sample_size = 1000', 'value': 1000},
                    {'label': 'sample_size = 500000', 'value': 500000},
                    {'label': 'sample_size = 500', 'value': 500}
                ],
                value=[100000,10000,1000,500000,500],
                labelStyle={'display': 'inline-block'}
            ),

            dcc.Checklist(
                id="Checklist_only_quanti",
                options=[
                    {'label': 'only quanti = True', 'value': True},
                    {'label': 'only quanti = False', 'value': False},
                ],
                value=[True,False],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Checklist(
            id="Checklist_inputer",
            options = [
            {'label': 'type = iterative', 'value': 'iterative'},
            {'label': 'type = simple', 'value': 'simple'},
            ],
            value=['iterative','simple'],
            labelStyle={'display': 'inline-block'}
        ),
        dcc.Graph(
            id='scatter_plot_score'
        )]
        return(children)
    else :
        children = [
            html.P(
                'Bonsoir'
            )]
        return children


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
             children="Bienvenue sur Too Good To Go Analytics ! "
                      "Commencez par choisir un onglet à visiter :",
            className="header-description",   
         ),
         dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
             dcc.Tab(label='Explicabilité globale', value='explicabilite-globale'),
             dcc.Tab(label='Explicabilité locale', value='explicabilite-locale'),
             dcc.Tab(label='Performances globales', value='performances-globales')
         ]),
         html.Div(
             children=[
                 html.P(
                     'Bonsoir'
             )],
             id='tabs-content-example'),
         ],
    className="header",
)
