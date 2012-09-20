import csv, re, string, json
import pprint as pp

def to_snake(s):
    return re.sub('\W', '_', s.lower()).replace('__', '_').strip('_')

f='./data/naics07.txt'

def read_rows(f):
    with open(f, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return [row for row in reader]


def get_records(rows):
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
    
rows = read_rows(f)

sample = rows[:10]

records = get_records(sample)

data = json.dumps(records)
pp.pprint(json.loads(data))

