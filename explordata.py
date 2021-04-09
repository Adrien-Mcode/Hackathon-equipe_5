# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 15:43:50 2021

Exploration et nettoyage des données

@author: Jérémie Stym-Popper
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

database = pd.read_csv(r"C:\Users\Asus\Desktop\Jérémie\Hackathon\train.csv")

database.drop(columns=['is_enabled', 'store_country', 'country_iso_code',
                       'currency_code'], inplace=True)

cancellation = database.groupby('store_id').sum().store_cancellation
cancellation = cancellation.sort_values(ascending=False)

supply = database.groupby('store_id').sum().total_supply

storexit = pd.DataFrame(database.groupby('store_id')['target'].nunique()).reset_index()

# Visualisation 

segment = database.groupby('store_segment').count()['store_id']

sns.countplot(data=database, x='store_segment', orient='v')
