from google.cloud import bigquery
client = bigquery.Client()

# DEFS

# Class implementation
class BigSQL():
    #def __init__(self):

    # get results
    def query(self, query_str):
        return client.query(query_str, location="US")

    def add_new(self, lang, long, height="0", speed="0", _type="1", age="5"):
        return None

    def get_now(self):
        return None

# for row in query_job:
              # Row values can be accessed by field name or index
##    assert row[0] == row.name == row["name"]
##    print(row)