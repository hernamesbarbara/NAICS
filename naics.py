import json
import pprint as pp
from pymongo import Connection
db = Connection()['industries']


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
