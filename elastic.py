from elasticsearch import Elasticsearch
import json
from pprint import pprint

def query_h1bdb(title):
    esclient = Elasticsearch(['localhost:9200'])

    title = "CHIEF OPERATING OFFICER"

    response = esclient.search(

    index='salaries',
    body={
        "query": {
            "match": {
                "TITLE": title
                }
            }
        }
    )

    print json.dumps(response, indent=4)
    pprint(response)