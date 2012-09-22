import json
import pprint as pp
from pymongo import Connection

naics_db = Connection()['industries']

class naics(object):
    def __init__(self, db=naics_db):
        self.db = db

    def find_all(self):
        codes = []
        for n in self.db.naics_2007.find():
            if "_id" in n:
                del n['_id']
            codes.append(n)
        return codes

    def find(self, naics_code):
        doc = self.db.naics_2007.find_one({"2007_naics_us_code":str(naics_code)})
        code = doc if doc else {}
        if "_id" in code:
            del code["_id"]
        return code
