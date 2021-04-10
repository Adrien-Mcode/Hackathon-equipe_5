# Mutual information sklearn Hackathon
import pandas as pd
import numpy as np
from sklearn.feature_selection import mutual_info_classif

df = pd.read_csv(r'C:\Users\Asus\Desktop\Jérémie\Hackathon\train.csv').sample(50000)

X = df[[
    'total_supply', 'declared_supply', 'manual_added_supply',
    'manual_removed_supply', 'meals_saved', 'consumer_cancellation',
    'store_cancellation', 'item_price', 'meals_refunded',
    'rating_count', 'sum_rating_overall'
    ]]

y = df['target']

X_corr = df[[
    'total_supply', 'declared_supply', 'manual_added_supply',
    'manual_removed_supply', 'meals_saved', 'consumer_cancellation',
    'store_cancellation', 'item_price', 'meals_refunded',
    'rating_count', 'sum_rating_overall', 'target'
    ]]

X_corr.shape

res = mutual_info_classif(X, y)
res2 = np.corrcoef(X_corr.T)


res2[:,11][:11]

df_mutual = pd.DataFrame(index=X.columns, columns=['mutual'], data=res)
df_mutual['corrcoef']=res2[:,11][:11]

df_mutual
