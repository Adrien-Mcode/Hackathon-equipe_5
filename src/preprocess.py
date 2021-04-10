import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import SimpleImputer, IterativeImputer
from sklearn.pipeline import Pipeline
import category_encoders as ce


def preprocess(df, config):
    if config.only_quantitative:
        df = df[[
            'total_supply', 'declared_supply', 'manual_added_supply',
            'manual_removed_supply', 'meals_saved', 'consumer_cancellation',
            'store_cancellation', 'item_price', 'meals_refunded',
            'rating_count', 'sum_rating_overall', 'target'
            ]]
    else:
    # Drop useless variable
        df = df.drop(columns=["country_iso_code", "store_country", "currency_code", "store_region"]) # "is_enabled",
        df.is_enabled = df.is_enabled.astype(int)
    # Convert date to int
        for col in ["date", "items_first_enabled_date", "store_first_saving_date", "store_last_saving_date"]:
            df[col] = pd.to_datetime(df[col])
            df[col] = (df[col] - df[col].min())/np.timedelta64(1,'D')

        for col in ["pickup_start", "pickup_end"]:
            df[col] = pd.to_datetime(df[col])
            df[col] = (df[col] - df[col].min())/np.timedelta64(1,'h')

    transformers_list = []
    # Encode qualitative data
    if config.target_encoding:
        enc = ce.TargetEncoder(cols=config.qualitative_cols)
        transformers_list.append(('cat', enc, list(config.qualitative_cols)))
    # Fill missing values

    if config.kind_imputer == "simple":
        imp = Pipeline([('imputer', SimpleImputer(strategy='mean'))])
        if config.target_encoding:
            transformers_list.append(('imp', imp, list(config.qualitative_cols) + list(config.quantitative_cols)))
        else:
            transformers_list.append(('imp', imp, list(config.qualitative_cols)))
    elif config.kind_imputer == "iterative":
        imp = Pipeline([('imputer', IterativeImputer())])
        if config.target_encoding:
            transformers_list.append(('imp', imp, list(config.qualitative_cols) + list(config.quantitative_cols)))
        else:
            transformers_list.append(('imp', imp, list(config.qualitative_cols)))
    if transformers_list:
        pipeline = [("col_trans", ColumnTransformer(transformers_list))]
    else:
        pipeline = []
    # Normalize
    # if config.standardize:
    #     scal = StandardScaler()
    # if config.minmax:
    #     scal = MinMaxScaler()

    return df, pipeline