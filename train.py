# Imports
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import gcsfs

# Import globals
import json
with open('./consts.json') as json_file:
    consts = json.load(json_file)
    fs = gcsfs.GCSFileSystem(project=consts["PROJECT"])

def init_data(file_path, time_col, select_col):
    with fs.open(file_path) as f:
        df = pd.read_csv(f)
        df = df[[time_col, select_col]][:-3000]
        df.columns = ['ds', 'y']
        df.head()

        return df

def get_prophet():
    return Prophet() \
        .add_seasonality(name="monthly", period=30.5, fourier_order=5) \
        .add_seasonality(name="yearly", period=365.25, fourier_order=5) \
        .add_seasonality(name="quarterly", period=365.25/4, fourier_order=5, prior_scale = 15)

def upload_results(results, _type):
    from datalab.context import Context

    #Alternative 1
    results.to_gbq('Predictions.%s' % _type, 
                    Context.default().project_id,
                    chunksize=10000, 
                    if_exists='replace',
                    verbose=False
    )

if __name__ == "__main__":
    for _type in ['lang', 'long']:
        
        # Get dataset and models
        print('[Model] Building sets and models [%s]...' % _type)
        df = init_data(consts["TRAINING_FILEPATH"], 'timestamp', _type)
        m = get_prophet()

        # Learn
        print('[Model] Applying fitting algorithms...')
        m.fit(df)

        # Predict future interval
        print('[Model] Predicting...')
        future = m.make_future_dataframe(periods=365)
        future.tail()

        forecast = m.predict(future)
        forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
        
        # make diags and build artifacts
        print('[Model] Building and packing...')
        fig = m.plot_components(forecast).savefig("%s.png" % _type)

        # reformat
        df.columns = [str(_type) + "_" + str(col) for col in df.columns]
        
        # upload
        upload_results(forecast, _type)