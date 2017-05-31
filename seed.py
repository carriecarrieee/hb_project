"""Seeds the salaries database into elasticsearch."""


from elasticsearch import helpers, Elasticsearch
import csv


esclient = Elasticsearch(['localhost:9200'])

def UnicodeDictReader(utf8_data, **kwargs):
    csv_reader = csv.DictReader(utf8_data, **kwargs)
    for row in csv_reader:
        row_obj = row.iteritems()
        doc = {unicode(key, 'utf-8'): unicode(value, 'utf-8') \
            for key, value in row_obj if key not in ["lon", "lat"]}

        # Create location dictionary that includes geopoint and coordinates.
        try:
            doc["location"] = {"lat": float(row["lat"]), "lon": float(row["lon"])}

            yield doc
        except:
            pass


with open('data/h1b_salaries.csv') as file:
    reader = UnicodeDictReader(file)
    helpers.bulk(esclient, reader, index='salaries', doc_type='h1b_apps')

