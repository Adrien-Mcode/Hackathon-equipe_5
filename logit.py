# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 17:17:59 2021

Régression logistique sur database

@author: Jérémie Stym-Popper
"""

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import balanced_accuracy_score, plot_confusion_matrix, recall_score, precision_score, f1_score, accuracy_score

database = pd.read_csv(r"C:\Users\Asus\Desktop\Jérémie\Hackathon\train.csv")

X = database[['total_supply', 'declared_supply', 'manual_added_supply', 
              'manual_removed_supply', 'meals_saved', 'consumer_cancellation', 
              'store_cancellation', 'item_price', 'meals_refunded', 
              'rating_count', 'sum_rating_overall']]
y = database.target

X_train, X_test, y_train, y_test = train_test_split(X, y)

clf = LogisticRegression(class_weight='balanced').fit(X_train, y_train)

clf.score(X_test, y_test)

metrics = [balanced_accuracy_score, recall_score, precision_score, f1_score, accuracy_score]

scores = [metric(y_test, clf.predict(X_test)) for metric in metrics]
balanced_accuracy_score(y_test, clf.predict(X_test))

plot_confusion_matrix(clf, X_test, y_test)

# Passage sur mlflow

import mlflow
