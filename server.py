from flask import Flask, jsonify
from flask import render_template, request, Response
import json, os
from naics import *

app = Flask(__name__)
Naics = naics()

@app.route("/naics/all", methods=['GET'])
def naics():
    return Response(json.dumps(Naics.find_all()), mimetype="application/json")

@app.route('/naics/<int:code>', methods=['GET'])
def find_one(code):
    docs = Naics.find(code)
    res = Response(json.dumps(docs), status=200, mimetype='application/json')
    res.headers['Title'] = 'NAICS 2007 Industry Codes'
    return res

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    #app.run(debug=True)

