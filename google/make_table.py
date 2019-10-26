# Imports
import matplotlib
matplotlib.use('Agg')
import pandas as pd
from fbprophet import Prophet
import matplotlib.pyplot as plt
import gcsfs

# Import globals
import json
with open('../consts.json') as json_file:
    consts = json.load(json_file)
    fs = gcsfs.GCSFileSystem(project=consts["PROJECT"])

def load_data(file_path):
    df = pd.read_csv(file_path)
    df.columns = ['timestamp', 'lang', 'long', 'height', 'speed', 'type', 'age']
    df.head()

    return df

def upload_results(results, table_name):
    from datalab.context import Context

    #Alternative 1
    results.to_gbq('Data.%s' % table_name, 
                    Context.default().project_id,
                    chunksize=10000, 
                    if_exists='replace',
                    verbose=False
    )

if __name__ == "__main__":
    df = load_data("../data/birds.csv")
    upload_results(df, "Birds")