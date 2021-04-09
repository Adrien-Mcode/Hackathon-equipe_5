from .raw import get_train
from .preprocess import preprocess
import mlflow
from .utils import save_mlflow_run_id, save_model
from .plot import log_stat_desc
from sklearn.linear_model import LogisticRegression
from .raw import get_our_test
import os
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, plot_confusion_matrix, \
    recall_score, precision_score, f1_score, accuracy_score


def do_training(config):
    run_name = config.model_name + str(config.nrows_train)
    with mlflow.start_run(run_name=run_name) as run:
        run_id = run.info.run_id
        save_mlflow_run_id(run_name, run_id, "save_mlflow_dict.yml")
        mlflow.log_artifact(config.config_filepath, "config")
        train_df = get_train(config)
        log_stat_desc()
        train_preprocess_df, inputers = preprocess(train_df, config)
        model = train(train_preprocess_df, inputers, config)
        eval(train_preprocess_df, model, config)

        our_test_df = get_our_test(config)
        our_test_preprocess_df, _ = preprocess(our_test_df, config)
        eval(our_test_preprocess_df, model, config, mode="test")


def train(train_df, inputers, config):
    if config.model_type == "logit":
        inputers.append(("logit", LogisticRegression(class_weight='balanced')))
    else:
        clf = None
    clf = Pipeline(inputers).fit(train_df.drop(["target"], axis=1), train_df["target"])
    mlflow.sklearn.log_model(clf, "TDJ forecast model")
    save_model(clf, config.model_filename)
    return clf


def eval(train_df, clf, config, mode="train"):
    y_pred = clf.predict(train_df.drop(["target"], axis=1))
    y_real = train_df["target"]
    metrics = [balanced_accuracy_score, recall_score, precision_score, f1_score, accuracy_score]
    scores = {metric.__name__: metric(y_real, y_pred) for metric in metrics}
    mlflow.log_metrics(scores)
    fig = plot_confusion_matrix(clf, train_df.drop(["target"], axis=1), y_real).plot().figure_
    filename = os.path.join(config.figure_folder, mode + "_confusion_matrix.png")
    fig.savefig(filename)
    mlflow.log_artifact(filename, "confusion_matrix")

