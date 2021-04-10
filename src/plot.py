import matplotlib.pyplot as plt
import numpy as np


def log_stat_desc():
    pass


def plot_feature_importance(clf, df):
    importances = clf.feature_importances_
    indices = np.argsort(importances)[::-1]

    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(df.shape[1]), importances[indices], color='r', yerr=std[indices], align='center')
    plt.xticks(range(df.shape[1]), indices)
    plt.xlim([-1, df.shape[1]])
    plt.show()

