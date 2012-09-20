import csv, re, string, json
import pprint as pp

def to_snake(s):
    return re.sub('\W', '_', s.lower()).replace('__', '_').strip('_')

f='./data/naics07.txt'

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

def get_records(rows):
    records = []
    for i, row in enumerate(rows):
        if i == 0:
            headers = [to_snake(field) for field in row]
            headers = dict(zip(headers, range(len(headers))))
            continue

        if all(map(lambda x: len(x)==0, row)):
            continue

        records.append(row)
        
    return records, headers

records, headers = get_records(read_rows(f))
data = json.dumps(records)

##with open('eggs.csv', 'wb') as csvfile:
##    outfile = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
##    outfile.writerow(headers.keys())
##    for r in records:
##        outfile.writerow(r)
