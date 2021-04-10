import mlflow
import pandas as pd
from src.preprocess import preprocess
import numpy as np
import json
from io import StringIO
import requests

def main():
    logged_model = 'file:///C:/Users/SURFACE/Documents/GitHub/Hackathon-equipe_5/lightgbm_500000_iterative_False_lightgbm'
    loaded_model = mlflow.sklearn.load_model(logged_model)
    test_df = pd.read_csv(r"C:\Users\SURFACE\Documents\Ensae\2A\Hackathon\SujetMachineLearning-TGTG\Sujet Machine Learning - TGTG\test.csv", parse_dates=["date", "items_first_enabled_date"])


    df = test_df[["date", "is_enabled", "items_first_enabled_date", "store_first_saving_date",
     "store_last_saving_date", "pickup_start", "pickup_end", "total_supply", "declared_supply",
     "manual_added_supply", "manual_removed_supply", "meals_saved", "consumer_cancellation",
     "store_cancellation", "item_price", "meals_refunded", "rating_count", "sum_rating_overall"]]
    df.is_enabled = df.is_enabled.astype(int)

# Convert date to int
    for col in ["date", "items_first_enabled_date", "store_first_saving_date", "store_last_saving_date"]:
        df[col] = pd.to_datetime(df[col])
        df[col] = (df[col] - df[col].min())/np.timedelta64(1,'D')

    for col in ["pickup_start", "pickup_end"]:
        df[col] = pd.to_datetime(df[col])
        df[col] = (df[col] - df[col].min())/np.timedelta64(1, 'h')
    url = "https://51.159.6.59:8798/"
    password = "Ensae06CPdist"
    res = loaded_model.predict(df)
    res_df = pd.DataFrame()
    res_df["target"] = res
    res_df_bis = pd.DataFrame(loaded_model.predict_proba(df), columns=["0", "1"])
    res_df["score"] = res_df_bis["1"]
    res_df["index"] = df.index
    print(res_df.shape)
    st = StringIO()
    res_df.to_csv(st, index=False, line_terminator="\n")

    data = {
      "name": "Lighty",
      "format": "df",
      "team": "Equipe 5",
      "project": "tgtg",
      "version": "1",
      "content": st.getvalue(),
      "password": password
    }
    import ipdb
    ipdb.set_trace()

    response = requests.post(url, json=data, verify=False)


if __name__ == "__main__":
    main()


