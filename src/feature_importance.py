import numpy as np
from sklearn.linear_model import LogisticRegression


def compute_feature_importance(clf, df):
    if not isinstance(clf["model"], LogisticRegression):
        importances = clf.feature_importances_
        # std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
        indices = np.argsort(importances)[::-1]
        print(indices)

        # Print the feature ranking
        print("Feature ranking:")

        for f in range(df.shape[1]):
            print(f"{f+1}. feature {indices[f]} : {df.columns[indices[f]-1]} ({importances[indices[f]]})")



