import csv, re, string, json
import pprint as pp

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
    f='./data/naics07.txt'
    naics = get_dicts(read_rows(f))
    return naics

def fetch_one(code):
    f='./data/naics07.txt'
    naics = get_dicts(read_rows(f))
    code_index = dict((n['2007_naics_us_code'], i) for i, n in enumerate(naics))
    if code_index.get(str(code), -1) != -1:
        return naics[code_index.get(str(code), -1)]
    else:
        return []
