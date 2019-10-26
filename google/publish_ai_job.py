import googleapiclient.discovery

# Create AI Training input specification
def generate_input_json(input_file, output_folder):
    return {
        "scaleTier": "CUSTOM",
        "masterType": "complex_model_m",
        "args": [
            "--preprocess",
            "--training_data_path={}".format(input_file),
            "--validation_split=0.3",
            "--test_split=0.1",
            "--objective=reg:linear",
            "--booster=gbtree",
            "--subsample=1",
            "--colsample_bytree=1",
            "--lambda=1",
            "--tree_method=auto",
            "--colsample_bylevel=1",
            "--scale_pos_weight=1",
            "--updater=grow_colmaker,prune",
            "--refresh_leaf=0",
            "--process_type=default",
            "--grow_policy=depthwise",
            "--num_boost_round=10",
            "--max_depth=6",
            "--eta=0.3",
            "--csv_weight=0",
            "--base_score=0.5"
        ],
        "region": "europe-west1",
        "jobDir": output_folder,
        "masterConfig": {
            "imageUri": "gcr.io/cloud-ml-algos/boosted_trees:latest"
        }
    }

def create_ai_job(project_name, job_name, input_file, output_folder):
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    cloudml = googleapiclient.discovery.build('ml', 'v1')
    project_id = 'projects/{}'.format(project_name)
    new_job_id = len(cloudml.projects().jobs().list(parent=project_id).execute()["jobs"])
    job = generate_input_json(
        input_file="gs://training-store-bucket/training/birds.csv", 
        output_folder="gs://training-store-bucket/trained/"
    )
    job_spec = {'jobId': job_name+"_"+str(new_job_id), 'trainingInput': job}

    # Send request
    request = cloudml.projects().jobs().create(
        body=job_spec,
        parent=project_id
    )
    response = request.execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    print(response)

if __name__ == "__main__":
    create_ai_job(
        project_name="crisis-257016",
        job_name="training_birds_3", 
        input_file="gs://training-store-bucket/training/birds.csv", 
        output_folder="gs://training-store-bucket/trained/"
    )