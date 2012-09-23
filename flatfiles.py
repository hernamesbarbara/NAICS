import csv, re, string, xlrd, codecs
import pprint as pp

from pymongo import Connection
db = Connection()['industries']


def utf8ify(a_list):
    "returns a new list with anything string-like replaced with a utf-8 string"
    """
    args: a_list:
        a list of items of any type 
        e.g. => [1.0, 11.0, u'Agriculture, Forestry, Fishing and Hunting']

    returns:
        [1.0, 11.0, 'Agriculture, Forestry, Fishing and Hunting']
    """
    return [unicode(s).encode("utf-8") if hasattr(s,'encode') else s for s in a_list]

def to_snake(s):
    "returns a string in snake_case"
    """    
    >>> to_snake('my phone number is (555)555-5555')
    'my_phone_number_is_555_555_5555'

    """
    return re.sub('\W', '_', s.lower()).replace('__', '_').strip('_') if hasattr(s, 'encode') else s

def read_txt(f):
    with open(f, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return [row for row in reader]

def read_xls(workbook, sheet_name='Sheet1'):
    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_name(sheet_name)
    records = []
    for i, r in enumerate(range(sh.nrows)):
        row = sh.row_values(r)
        row = utf8ify(row)
        records.append(row)
    return records

def lists_to_dicts(list_of_lists, headers_index=0):
    "given a list of lists, returns a list of dictionaries"
    """
    args:
        list_of_lists: [ ['item1', 'item2'], ['item3', 'item4'] ]
        headers_index: int => index of the row to become dictionary keys
    returns:
        list of dictionaries
        records: [{key1: 'item1', key2: 'item2'},{key1: 'item3', key2: 'item4'}]
    """
    headers_index = headers_index
    rows = list_of_lists
    records = []
    
    for i, row in enumerate(rows):

        if i < headers_index:
            continue
        
        if i==headers_index:
            headers = [to_snake(field) for field in utf8ify(row)]
            headers = dict(zip(headers, range(len(headers))))
            continue

        if all(map(lambda x: len(str(x))==0, row)):
            continue

        record = {}
        for field_name in headers.keys():
            record[field_name] = row[headers[field_name]]
        records.append(record)
        
    return records


def save_to_mongo(records, db, collection):
    "save a list of dictionaries to mongo"
    
    """
    args:
        records: [{'foo': 'bar'}, {'something': 'somethingelse'}]
        db: mongodb = Connection()['industries']
        collection: name of the collection
    """
    for doc in records:
        db.collection.save(doc)


def main():
    txt_file='./data/naics07.txt'
    workbook = './data/2-digit_2012_Codes.xls'
    sheet = 'tbl_2012_title_description_coun'

    xls_rows = read_xls(workbook=workbook, sheet_name=sheet)
    txt_rows = read_txt(txt_file)

    naics_2007 = lists_to_dicts(txt_rows)
    naics_2012 = lists_to_dicts(xls_rows)
    return (naics_2007, naics_2012)


data = main()
