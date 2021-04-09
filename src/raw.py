import pandas as pd
import random
import numpy as np
import os

filename = "data.txt"
n = sum(1 for line in open(filename)) - 1 #number of records in file (excludes header)
s = n_rows#desired sample size
skip = sorted(random.sample(range(1,n+1),n-s)) #the 0-indexed header will not be included in the skip list
df = pd.read_csv(filename, skiprows=skip)


def generate_train(config):
    n = sum(1 for line in open("train.csv")) - 1  # number of records in file (excludes header)
    s = config.nrows_train
    skip = sorted(random.sample(range(1, n + 1), n - s))  # the 0-indexed header will not be included in the skip list
    df = pd.read_csv("train.csv", parse_dates=["date", "items_first_enabled_date"], skiprows=skip)
    msk = np.random.rand(len(df)) < config.split_ratio
    train = df[msk]
    our_test = df[~msk]
    return train, our_test

def get_train(config):
    filename_train = os.path.join(os.getcwd(), config.sample_name + str(config.nrows) + ".csv")
    filename_test =
    if config.get_new or not os.path.isfile():
        train, our_test = generate_train(config)
        df.to_csv(filename)
    else:
        pd.read_csv("train.csv", parse_dates=["date", "items_first_enabled_date"], skiprows=skip)

def get_test(config):
    if not config.full_test:
        n = sum(1 for line in open("train.csv")) - 1  # number of records in file (excludes header)
        s = config.nrows_test
        skip = sorted(random.sample(range(1, n + 1), n - s))
        df = pd.read_csv("train.csv", parse_dates=["date", "items_first_enabled_date"], skiprows=skip)
    else:
        df = pd.read_csv("test.csv", parse_dates=["date", "items_first_enabled_date"])