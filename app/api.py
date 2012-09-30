#!/usr/bin/env python
from pymongo import Connection
from flask import Flask, jsonify
from flask import request, Response, redirect
import json, os, sys

#CONFIGS
app = Flask(__name__)
app.debug=False

mongo_url = os.environ.get('MONGOLAB_URI', 'mongodb://heroku_app8020356')


db_name = 'industries'


def get_query(params):
    year = int(params['year']) if 'year' in params else False
    code = int(params['code']) if 'code' in params else False
    
    if year:
        query = {"year": year}

    if code:
        query = {"code": code}

    if year and code:
        query = {"year": year, "code": code}

    return query

def find_naics(query={}):
    data = [rm_objectid(doc) for doc in db.naics_codes.find(query)]
    return {'objects': rm_objectid(data)}

def respond_with(body={}, status=200):
    res = jsonify(body)
    res.headers['Title'] = title()
    res.status_code = status
    return res

#HELPERS
def rm_objectid(doc={}):
    "remove mongo objectid to serialize"
    if "_id" in doc:
        del doc['_id']
    return doc

def title():
    return 'NAICS Industry Codes'

@app.before_request
def strip_trailing_slash():
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1])

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: %s' %(request.url)}
    return respond_with(message, 404)

#ROUTES

@app.route("/naics", methods=['GET'])
def get():
    query = False
    if len(request.args.keys()) > 0:
        query = get_query(request.args)
    data = find_naics(query) if query else find_naics()
    return respond_with(data, 200)

@app.route("/", methods=['GET'])
def root():
    message = {'status': 'OK',
               'name': 'NAICS Industry Codes',
               'version': '0.1',
               'url': 'http://github.com/hernamesbarbara/NAICS',
               'license': 'None',
               'author': 'Austin Ogilvie',
               'description': 'An API providing NAICS industry classification codes.'}
    
    return respond_with(message, 200)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    try:
        connection = pymongo.Connection(mongo_url)
        if 'localhost' in self.mongo_url:
            db_name = 'my_local_db_name'
        else:
            db_name = self.mongo_url.rsplit('/',1)[1]
            db = connection[db_name]

        app.run(host='0.0.0.0', port=port)
    except:
        print('Error: Unable to Connect')
        sys.exit("Unable to connect to the database")
