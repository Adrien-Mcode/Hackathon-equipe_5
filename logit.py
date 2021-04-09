# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 17:17:59 2021

Régression logistique sur database

@author: Jérémie Stym-Popper
"""

import pandas as pd
import matplotlib.pyplot as plt


database = pd.read_csv(r"C:\Users\Asus\Desktop\Jérémie\Hackathon\train.csv")

X = database[['total_supply', 'declared_supply', 'manual_added_supply', 
              'manual_removed_supply', 'meals_saved', 'consumer_cancellation', 
              'store_cancellation', 'item_price', 'meals_refunded', 
              'rating_count', 'sum_rating_overall']]
y = database.target

X_train, X_test, y_train, y_test = train_test_split(X, y)




# Passage sur mlflow

import mlflow
