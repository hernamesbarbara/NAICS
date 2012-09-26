from pymongo import Connection
from flask import Flask, jsonify
from flask import request, Response, redirect
import json, os

#CONFIGS
app = Flask(__name__)
app.debug=True
db = Connection()['industries']


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
    year_key = '%s_naics_us_code' %(str(request.args['year'])) if 'year' in request.args else False
    naics = int(request.args['code']) if 'code' in request.args else False
    query = False
    
    if year_key:
        query = {year_key: { '$exists' : 'true' }}

    if year_key and naics:
        query = {year_key: naics}

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

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
