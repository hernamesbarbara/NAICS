from flask import Flask, jsonify
from flask import request, Response
import json, os
import naics

app = Flask(__name__)
app.debug=True
db = naics.db_conn()

@app.errorhandler(404)
def not_found(error=None):
    message = {'status': 404, 'message': 'Not Found: %s' %(request.url)}
    res = jsonify(message)
    res.headers['Title'] = 'NAICS 2007 Industry Codes'
    res.status_code = 404
    return res

@app.route("/naics/all", methods=['GET'])
def find():
    data = db.find_all()
    res = jsonify(data)
    res.status_code = 200
    return res

@app.route('/naics/<int:code>', methods=['GET'])
def find_one(code):
    data = db.find(code)
    if len(data['objects'][0])==0:
        return not_found()
    else:
        res = jsonify(data)
        res.status_code = 200
        return res

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
