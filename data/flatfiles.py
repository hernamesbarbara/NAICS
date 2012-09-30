import csv, re, json, xlrd, codecs, sys
import pprint as pp
from pymongo import Connection
from urlparse import urlparse
import argparse

def utf8ify(a_list):
    "returns list w/ string as utf-8 and floats as ints"
    """
    >>> utf8ify([1.0, 11.0, u'Agriculture, Forestry, Fishing and Hunting'])
    ['1', '11', 'Agriculture, Forestry, Fishing and Hunting']
        
    """
    return [unicode(s).encode("utf-8") if hasattr(s,'encode') else int(s) for s in a_list]

def to_snake(s):
    "returns a string in snake_case"
    """    
    >>> to_snake('my phone number is (555)555-5555')
    'my_phone_number_is_555_555_5555'

    """
    return re.sub('\W', '_', s.lower()).strip('_').replace('__', '_') if hasattr(s, 'encode') else s

def read_txt(f):
    with open(f, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        return [utf8ify(row) for row in reader]

def read_xls(workbook, sheet_name='Sheet1'):
    wb = xlrd.open_workbook(workbook)
    sh = wb.sheet_by_name(sheet_name)
    return [utf8ify(sh.row_values(r)) for r in range(sh.nrows)]

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
            headers = [to_snake(field).replace('__', '_') for field in utf8ify(row)]
            headers = dict(zip(headers, range(len(headers))))
            continue

        if all(map(lambda x: len(str(x))==0, row)):
            continue

        record = {}
        for field_name in headers.keys():
            try:
                record[field_name] = int(row[headers[field_name]])
            except:
                record[field_name] = row[headers[field_name]]
                
        records.append(record)
        
    return records

def format_doc(doc):
    to_save={}
    
    for key in doc:
        print key, doc[key]
        if "_naics_us_title" in key:
            to_save["year"] = int(key[0:4])
            to_save["title"] = doc[key]

        if "_naics_us_code" in key:
            try:
                to_save["code"] = int(doc[key])
            except:
                to_save["code"] = int(doc[key][:2])

    return to_save


def save_to_mongo(records, db, collection):
    "save a list of dictionaries to mongo"
    
    """
    args:
        records: [{'foo': 'bar'}, {'something': 'somethingelse'}]
        db: mongodb = Connection()['industries']
        collection: name of the collection
    """

    print 'saving %s records to the %s mongo collection...' %(len(records), collection)
    for doc in records:
        doc = format_doc(doc)
        db['naics_codes'].save(doc)


def main():
    parser = argparse.ArgumentParser(description=('Given a URI and a file, saves data from the file to MongoDb.'))
    parser.add_argument('-m', '--mongodb', type=str, help='MONGO_URI')
    parser.add_argument('-f', '--filename', type=str, help='filename')
    parser.add_argument('-s', '--sheetname', type=str, default=None, help='sheetname if processing xls')
    parser.add_argument('-c', '--collection', type=str, help='mongo collection name')

    args = parser.parse_args()

    #files
    filename = args.filename
    sheetname = args.sheetname
    collection = args.collection

    #db
    MONGO_URI = args.mongodb
    try:
        uri = urlparse(MONGO_URI)
        db = Connection(MONGO_URI)[uri.path[1:]]
    except:
        sys.exit('unable to connect to the database')

    if filename.endswith('.txt'):
        rows = read_txt(filename)

    elif filename.endswith('xls'):
        if sheetname is not None:
            rows = read_xls(filename, sheetname)
        else:
            sys.exit('Provide a sheetname if processing xls file')

    else:
        sys.exit('Unable to process file. Please use .txt or .xls only')

    if rows:
        row_dicts = lists_to_dicts(rows)
        save_to_mongo(row_dicts, db, collection)

if __name__=='__main__':
    main()
