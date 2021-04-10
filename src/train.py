from .raw import get_train
from .preprocess import preprocess
import mlflow
from .utils import save_mlflow_run_id, save_model
from .plot import log_stat_desc
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from .raw import get_our_test
import os
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, plot_confusion_matrix, \
    recall_score, precision_score, f1_score, accuracy_score
from sklearn.model_selection import RandomizedSearchCV
import pandas as pd

from .feature_importance import compute_feature_importance
import lightgbm as lgb


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
        inputers.append(("model", LogisticRegression(class_weight='balanced')))
    elif config.model_type == "rfc":
        inputers.append(("model", RandomForestClassifier(class_weight='balanced')))
    elif config.model_type == "lightgbm":
        inputers.append(("model", lgb.LGBMClassifier(objective='binary', class_weight='balanced')))
    elif config.model_type == "lightgrid":

        param_grid = {
            'num_leaves': [50, 100, 200, 300],
            'min_data_in_leaf': [5, 7, 10, 20, 30, 50, 100],
            'max_depth': [4, 6, 8, 10],
            'learning_rate': [0.01, 0.005, 0.001],
            'boosting_type': ['gbdt', "dart"]
        }
        model = lgb.LGBMClassifier(objective='binary', class_weight='balanced', num_iterations=2000)
        gsearch = RandomizedSearchCV(model, param_grid, n_iter=20, n_jobs=4, verbose=True)
        inputers.append(("model", gsearch))

    else:
        clf = None

    clf = Pipeline(inputers).fit(train_df.drop(["target"], axis=1), train_df["target"])
    mlflow.sklearn.log_model(clf, f"{config.model_name}_{config.model_type}")
    save_model(clf, config.model_filename)
    return clf


def eval(df, clf, config, mode="train"):

    y_pred = clf.predict(df.drop(["target"], axis=1))
    y_real = df["target"]
    metrics = [balanced_accuracy_score, recall_score, precision_score, f1_score, accuracy_score]
    scores = {metric.__name__: metric(y_real, y_pred) for metric in metrics}
    mlflow.log_metrics(scores)
    scores = pd.DataFrame.from_dict(scores, orient='index', columns=["feature_importance"])
    filename = os.path.join(config.csv_folder, mode + "_scores.csv")
    scores.to_csv(filename)

    conf_matrix = confusion_matrix(y_real, y_pred)
    conf_matrix = pd.DataFrame(conf_matrix, index=["No churn", "Churn"], columns=["No churn", "Churn"])
    filename = os.path.join(config.csv_folder, mode + "_confusion_matrix.csv")
    conf_matrix.to_csv(filename)
    mlflow.log_artifact(filename, "csv")
    importance_df = compute_feature_importance(clf, df)
    filename = os.path.join(config.csv_folder, mode + "_feature_importance.csv")
    importance_df.to_csv(filename)
    mlflow.log_artifact(filename, "csv")

