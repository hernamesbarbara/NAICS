import csv, re, string

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


def read_file(f):
    return get_dicts(read_rows(f))

def save_to_mongo(records, db, collection):
    """save a list of dictionaries to mongo
    args:
        records: [{'foo': 'bar'}, {'something': 'somethingelse'}]
        db: mongodb = Connection()['industries']
        collection: name of the collection
    """
    for doc in records:
        db.collection.save(doc)

f='./data/naics07.txt'
