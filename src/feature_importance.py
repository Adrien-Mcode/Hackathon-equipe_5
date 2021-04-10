import numpy as np
from sklearn.metrics import balanced_accuracy_score
import pandas as pd

def compute_feature_importance(rf, df):

    def permutation_importances(rf, df):
        y_pred = rf.predict(df.drop(["target"], axis=1))
        y_train = df["target"]
        X_train = df.drop(["target"], axis=1)
        baseline = balanced_accuracy_score(y_pred, y_train)
        imp = {}
        for col in X_train.columns.values:
            save = X_train[col].copy()
            X_train[col] = np.random.permutation(X_train[col])
            y_pred = rf.predict(X_train)
            m = balanced_accuracy_score(y_train, y_pred)
            X_train[col] = save
            imp[col] = baseline - m
        return imp
    imp = permutation_importances(rf, df)
    imp = pd.DataFrame.from_dict(imp, orient='index', columns=["feature_importance"])
    return imp



