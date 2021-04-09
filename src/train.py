from .raw import get_train
from .preprocess import preprocess
import mlflow


def do_training(config):
    df = get_train(config.nrows)
    df = preprocess(df, config)
    train(df, config)


def train(df, config):
    pass