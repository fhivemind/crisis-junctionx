from google.cloud import bigquery
client = bigquery.Client()

query = (
    "SELECT name FROM `bigquery-public-data.usa_names.usa_1910_2013` "
    'WHERE state = "TX" '
    "LIMIT 100"
)
query_job = client.query(
    query,
    location="US",
) 

for row in query_job:  # API request - fetches results
    # Row values can be accessed by field name or index
    assert row[0] == row.name == row["name"]
    print(row)