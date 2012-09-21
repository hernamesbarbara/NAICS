import csv, re, string, json
import pprint as pp
from pymongo import Connection
db = Connection()['industries']

def to_snake(s):
    return re.sub('\W', '_', s.lower()).replace('__', '_').strip('_')

def read_rows(f):
    with open(f, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return [row for row in reader]

def get_dicts(rows):
    records = []
    for i, row in enumerate(rows):
        if i == 0:
            headers = [to_snake(field) for field in row]
            headers = dict(zip(headers, range(len(headers))))
            continue

        if all(map(lambda x: len(x)==0, row)):
            continue

        record = {}
        for field_name in headers.keys():
            record[field_name] = row[headers[field_name]]
        records.append(record)
    return records


def fetch_naics():
    naics = []
    for n in db.naics_2007.find():
        del n['_id']
        naics.append(n)
    return naics

def fetch_one(code):
    doc = db.naics_2007.find_one({"2007_naics_us_code":str(code)})
    if "_id" in doc:
        del doc["_id"]
    return doc
