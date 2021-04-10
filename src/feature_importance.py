import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

df1 = pd.read_csv('train.csv')

X = df1[['total_supply', 'declared_supply', 'manual_added_supply', 'store_id',
                      'manual_removed_supply', 'meals_saved', 'consumer_cancellation',
                      'store_cancellation', 'item_price', 'meals_refunded',
                      'rating_count', 'sum_rating_overall', 'target']]
y = df1.target

X_train, X_test, y_train, y_test = train_test_split(X,y)

forest = RandomForestClassifier().fit(X_train, y_train)

def compute_feature_importance(clf, df):
    importances = clf.feature_importances_
    # std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)
    indices = np.argsort(importances)[::-1]
    print(indices)

    # Print the feature ranking
    print("Feature ranking:")

    for f in range(df.shape[1]):
        print(f"{f+1}. feature {indices[f]} : {df.columns[indices[f]-1]} ({importances[indices[f]]})")


compute_feature_importance(forest, X)



