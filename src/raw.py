import pandas as pd
import random
import numpy as np
import os


def generate_train(config):
    # TODO : utiliser train_test_split
    n = sum(1 for line in open("train.csv")) - 1  # number of records in file (excludes header)
    s = config.nrows_train
    skip = sorted(random.sample(range(1, n + 1), n - s))  # the 0-indexed header will not be included in the skip list
    df = pd.read_csv("train.csv", parse_dates=["date", "items_first_enabled_date"], skiprows=skip)
    msk = np.random.rand(len(df)) < config.split_ratio
    train_df = df[msk]
    our_test = df[~msk]
    return train_df, our_test


def get_train(config):
    filename_train = os.path.join(os.getcwd(), "train_" + config.sample_name + "_" + str(config.nrows_train) + ".csv")
    filename_our_test = os.path.join(os.getcwd(),
                                     "our_test_" + config.sample_name + "_" + str(config.nrows_train) + ".csv")
    if config.get_new or not os.path.isfile(filename_train):
        train_df, our_test_df = generate_train(config)
        train_df.to_csv(filename_train)
        our_test_df.to_csv(filename_our_test)
    else:
        train_df = pd.read_csv(filename_train,
                               parse_dates=["date", "items_first_enabled_date"])
    return train_df


def get_our_test(config):
    filename_train = os.path.join(os.getcwd(), "train_" + config.sample_name + "_" + str(config.nrows_train) + ".csv")
    filename_our_test = os.path.join(os.getcwd(),
                                     "our_test_" + config.sample_name + "_" + str(config.nrows_train) + ".csv")
    if config.get_new or not os.path.isfile(filename_train):
        train_df, our_test_df = generate_train(config)
        train_df.to_csv(filename_train)
        our_test_df.to_csv(filename_train)
    else:
        our_test_df = pd.read_csv(filename_our_test,
                                  parse_dates=["date", "items_first_enabled_date"])
    return our_test_df


def get_test(config):
    if not config.full_test:
        n = sum(1 for line in open("train.csv")) - 1  # number of records in file (excludes header)
        s = config.nrows_test
        skip = sorted(random.sample(range(1, n + 1), n - s))
        test_df = pd.read_csv("train.csv", parse_dates=["date", "items_first_enabled_date"], skiprows=skip)
    else:
        test_df = pd.read_csv("test.csv", parse_dates=["date", "items_first_enabled_date"])
    return test_df