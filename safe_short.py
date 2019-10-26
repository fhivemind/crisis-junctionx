import os
import json
import time
import math
import matplotlib
matplotlib.use('Agg')

from sktime.forecasters import DummyForecaster
from sktime.forecasters import ARIMAForecaster
from sktime.forecasters import ExpSmoothingForecaster
from sktime.forecasters import EnsembleForecaster
from sktime.highlevel.tasks import ForecastingTask
from sktime.highlevel.strategies import ForecastingStrategy
from sktime.highlevel.strategies import Forecasting2TSRReductionStrategy
from sktime.datasets import load_shampoo_sales
from sktime.datasets import load_longley
from sktime.transformers.compose import Tabulariser
from sktime.pipeline import Pipeline

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from warnings import filterwarnings

from pprint import pprint

filterwarnings(action='ignore', category=FutureWarning, module='statsmodels')

shampoo = load_shampoo_sales()
s = shampoo.iloc[0]
s.head()


fig, ax = plt.subplots(1, figsize=plt.figaspect(.25))
s.plot(ax=ax)
ax.set(ylabel=s.name)

# split data into train, update and test

dataframe = pd.read_csv("data/go_track_trackspoints.csv")
pprint(dataframe.iloc[:,1].iloc[:30])
#dataframe.iloc[:,1].iloc[:30]
train = pd.Series([dataframe.iloc[:,1].iloc[:300]])
test = pd.Series([dataframe.iloc[:,1].iloc[300:400]])

fig, ax = plt.subplots(1, figsize=plt.figaspect(.25))
train.iloc[0].plot(ax=ax, label='train')
test.iloc[0].plot(ax=ax, label='test')
ax.set(ylabel=s.name)
plt.legend()

# arima model
order = (3, 2, 1)
m = ARIMAForecaster(order=order)
m.fit(train)

fh = np.arange(1, 100)
y_pred = m.predict(fh=fh)

# evaluate forecasts using default scorer (root mean squared error)
#m.score(test, fh=fh)

fig, ax = plt.subplots(1, figsize=plt.figaspect(.25))
train.iloc[0].plot(ax=ax, label='train')
test.iloc[0].plot(ax=ax, label='test')
y_pred.plot(ax=ax, label='forecast')
ax.set(ylabel=s.name)
plt.legend()


estimators = [
    ('ses', ExpSmoothingForecaster()), 
    ('holt', ExpSmoothingForecaster(trend='additive')), 
    ('damped', ExpSmoothingForecaster(trend='additive', damped=True))
]
m = EnsembleForecaster(estimators=estimators)
m.fit(train)
#m.score(test, fh=fh)

# simple exponential smoothing
m = ExpSmoothingForecaster()
m.fit(train)
m.get_params()

# automatically fitted param
m._fitted_estimator.params['smoothing_level']

m.set_params(**{'smoothing_level': .75})
m.fit(train)
#m.score(test, fh=fh)

# user given fixed parameter
m._fitted_estimator.params['smoothing_level']

plt.savefig("FIG.png")