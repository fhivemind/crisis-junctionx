# Import libraries
import warnings
import itertools
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statsmodels.api as sm

# Defaults
plt.rcParams['figure.figsize'] = (20.0, 10.0)
plt.rcParams.update({'font.size': 12})
plt.style.use('ggplot')

# Load the data
data = pd.read_csv('data/gps.csv', engine='python')
data = data.drop(["long", "frame", "id"], axis=1)

# A bit of pre-processing to make it nicer
data['timestamp']=pd.to_datetime(data['timestamp'], format='%Y-%m-%d %H:%M:%S')
data.set_index(['timestamp'], inplace=True)

# Plot the data
data.plot()
plt.ylabel('Lang')
plt.xlabel('Date')
plt.savefig("Base.png")


q = d = range(0, 2)
# Define the p parameters to take any value between 0 and 3
p = range(0, 4)

# Generate all different combinations of p, q and q triplets
pdq = list(itertools.product(p, d, q))

# Generate all different combinations of seasonal p, q and q triplets
seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

print('Examples of parameter combinations for Seasonal ARIMA...')
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

# Configure sets
train_data = data[0:14000]
test_data = data[14000:]

# specify to ignore warning messages
warnings.filterwarnings("ignore")

# start building models
AIC = []
SARIMAX_model = []
for param in pdq:
    for param_seasonal in seasonal_pdq:
        try:
            mod = sm.tsa.statespace.SARIMAX(train_data,
                                            order=param,
                                            seasonal_order=param_seasonal,
                                            enforce_stationarity=False,
                                            enforce_invertibility=False)

            results = mod.fit()

            print('SARIMAX{}x{} - AIC:{}'.format(param, param_seasonal, results.aic), end='\r')
            AIC.append(results.aic)
            SARIMAX_model.append([param, param_seasonal])
        except:
            continue
print('The smallest AIC is {} for model SARIMAX{}x{}'.format(min(AIC), SARIMAX_model[AIC.index(min(AIC))][0],SARIMAX_model[AIC.index(min(AIC))][1]))

# fit model
mod = sm.tsa.statespace.SARIMAX(train_data,
                                order=SARIMAX_model[AIC.index(min(AIC))][0],
                                seasonal_order=SARIMAX_model[AIC.index(min(AIC))][1],
                                enforce_stationarity=False,
                                enforce_invertibility=False)

results = mod.fit()
results.plot_diagnostics(figsize=(20, 14))
plt.savefig("diag.png")

# predict data that the model was built on
# 1-step ahead forecasting implies that each forecasted point is used to predict the following one.
pred0 = results.get_prediction(start='2015-06-05 13:16:38', dynamic=False)
pred0_ci = pred0.conf_int()

# n sample prediction with dynamic forecasting of the last year 
# the model is used to predict data that the model was built on
pred1 = results.get_prediction(start='2015-06-05 13:16:38', dynamic=True)
pred1_ci = pred1.conf_int()

# "True" forecasting of out of sample data 
# the model is asked to predict data it has not seen before.
pred2 = results.get_forecast('2015-06-05 13:16:38')
pred2_ci = pred2.conf_int()
print(pred2.predicted_mean['2016-01-19 13:01:47':'2017-01-19 13:01:47'])

# plot
ax = data.plot(figsize=(20, 16))
pred0.predicted_mean.plot(ax=ax, label='1-step-ahead Forecast (get_predictions, dynamic=False)')
pred1.predicted_mean.plot(ax=ax, label='Dynamic Forecast (get_predictions, dynamic=True)')
pred2.predicted_mean.plot(ax=ax, label='Dynamic Forecast (get_forecast)')
ax.fill_between(pred2_ci.index, pred2_ci.iloc[:, 0], pred2_ci.iloc[:, 1], color='k', alpha=.1)
plt.ylabel('Lang')
plt.xlabel('Date')
plt.legend()
plt.savefig("out.png")

prediction = pred2.predicted_mean['2016-01-19 13:01:47':'2017-01-19 13:01:47'].values


# flatten nested list
truth = list(itertools.chain.from_iterable(test_data.values))
# Mean Absolute Percentage Error
MAPE = np.mean(np.abs((truth - prediction) / truth)) * 100

print('The Mean Absolute Percentage Error for the forecast of year 2016 is {:.2f}%'.format(MAPE))
