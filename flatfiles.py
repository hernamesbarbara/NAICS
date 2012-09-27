import csv, re, json, xlrd, codecs
import pprint as pp

from pymongo import Connection
db = Connection()['industries']


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


def main(__name__):
    naics_2007_txt ='./data/naics07.txt'
    naics_2012_xls = './data/2-digit_2012_Codes.xls'
    naics_2012_sheet = 'tbl_2012_title_description_coun'

    naics_2007 = read_txt(naics_2007_txt)
    naics_2012 = read_xls(workbook=naics_2012_xls, sheet_name=naics_2012_sheet)

    naics_2007 = lists_to_dicts(naics_2007)
    naics_2012 = lists_to_dicts(naics_2012)

    conn = Connection()['industries']
    
    save_to_mongo(naics_2007, conn, 'naics_codes')
    save_to_mongo(naics_2012, conn, 'naics_codes')

if __name__=='__main__':
    main(__name__)
