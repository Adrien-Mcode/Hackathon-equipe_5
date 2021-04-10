import mlflow
import pandas as pd
import shap
import matplotlib.pyplot as plt
import numpy as np
from io import BytesIO
import base64

logged_model = 'file:///C:/Users/SURFACE/Documents/GitHub/Hackathon-equipe_5/lightgbm_500000_iterative_False_lightgbm'

data = pd.read_csv(r'..\..\df_petit.csv', parse_dates=["date", "items_first_enabled_date"])
# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)

# Predict on a Pandas DataFrame.
import dash
import dash_core_components as dcc
import dash_html_components as html
from src.dash.app import app
import datetime as dt
from dash.dependencies import Input, Output

shap_layout = [
        dcc.Slider(id="slider-shap",
            min=0,
            max=10,
            step=None,
            marks={store_id: str(store_id) for store_id in data.store_id.unique()},
            value=data.store_id.unique()[0]),


        dcc.DatePickerRange(
            id="date-range",
            min_date_allowed=data.date.min(),
            max_date_allowed=data.date.max(),
            start_date=data.date.min(),
            end_date=data.date.min(),
        ),

        html.Img(id="shap",
            height='auto',
            width='auto',
        )
    ]


@app.callback(Output("shap", "src"), [Input("startdate-input", "value"), Input("slider-shap", "value")])
def shap_predict(date_value, id_value):
    current = data[(data["date"].isin(date_value)) & (data["store_id"] == id_value)]
    explainer = shap.TreeExplainer(loaded_model)
    shap_values = explainer.shap_values(current.drop(["target"], axis=1))
    shap.plots.waterfall(shap_values[0])
    fig = plt.gcf()
    plt.close()
    return fig_to_uri(in_fig=fig)


def fig_to_uri(in_fig, close_all=True, **save_args):
    """
    Save a figure as a URI
    :param in_fig:
    :return:
    """
    out_img = BytesIO()
    in_fig.savefig(out_img, format='png', **save_args)
    if close_all:
        in_fig.clf()
        plt.close('all')
    out_img.seek(0)  # rewind file
    encoded = base64.b64encode(out_img.read()).decode("ascii").replace("\n", "")
    return "data:image/png;base64,{}".format(encoded)

