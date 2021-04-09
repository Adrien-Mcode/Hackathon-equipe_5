import pandas as pd


def get_train(n_rows=None):
    if n_rows is not None:
        df = pd.read_csv("train.csv", nrows=n_rows, parse_dates=["date", "items_first_enabled_date"])
    else:
        df = pd.read_csv("train.csv", parse_dates=["date", "items_first_enabled_date"])


def get_test(n_rows):
    if n_rows is not None:
        df = pd.read_csv("test.csv", nrows=n_rows, parse_dates=["date", "items_first_enabled_date"])
    else:
        df = pd.read_csv("test.csv", parse_dates=["date", "items_first_enabled_date"])