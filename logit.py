# -*- coding: utf-8 -*-
"""
Created on Fri Apr  9 17:17:59 2021

Régression logistique sur database

@author: Jérémie Stym-Popper
"""

import pandas as pd
import matplotlib.pyplot as plt


database = pd.read_csv(r"C:\Users\Asus\Desktop\Jérémie\Hackathon\train.csv")


y = database.target

X_train, X_test, y_train, y_test = train_test_split(X, y)




# Passage sur mlflow

import mlflow
