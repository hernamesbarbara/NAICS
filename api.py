from flask import Flask, jsonify, g
from flask import request, Response, redirect
import json, os
import naics

app = Flask(__name__)
app.debug=True

#CONFIGS

def connect_db():
    return naics.mongo_db()

def title():
    return 'NAICS 2007 Industry Codes'

#HELPERS

@app.before_request
def before_request():
    g.db = connect_db()

@app.before_request
def strip_trailing_slash():
    if request.path != '/' and request.path.endswith('/'):
        return redirect(request.path[:-1])

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: %s' %(request.url)}
    res = jsonify(message)
    res.headers['Title'] = title()
    res.status_code = 404
    return res

#ROUTES

@app.route("/", methods=['GET'])
def root():
    message = {'status': 'OK',
               'name': 'NAICS 2007 Industry Codes',
               'version': '0.1',
               'url': 'http://github.com/hernamesbarbara/NAICS',
               'license': 'None',
               'author': 'Austin Ogilvie',
               'description': 'An API providing the 2007 NAICS industry classification codes.'}
    
    res = jsonify(message)
    res.headers['Title'] = title()
    res.status_code = 200
    return res

@app.route("/naics/all", methods=['GET'])
def find():
    data = g.db.find()
    res = jsonify(data)
    res.headers['Title'] = title()
    res.status_code = 200
    return res

@app.route('/naics/<int:code>', methods=['GET'])
def find_one(code):
    data = g.db.find_one(code)
    if len(data['objects'][0])==0:
        return not_found()
    else:
        res = jsonify(data)
        res.headers['Title'] = title()
        res.status_code = 200
        return res

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
