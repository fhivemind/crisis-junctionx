import os
import glob
from google.cloud import storage

# Import globals
import json
with open('../consts.json') as json_file:
    consts = json.load(json_file)

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""
    storage_client = storage.Client.from_service_account_json(
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"])

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    #returns a public url
    return blob.public_url


if __name__ == "__main__":
    for file in glob.glob('../data/*.csv'):
        print("Uploading file %s" % file)
        print(upload_to_bucket("training/{}".format(os.path.basename(file)), file, consts["TRAINING_BUCKET"]))
